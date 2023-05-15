from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
from django.db import IntegrityError
from django.urls import reverse_lazy
from .filters import ProfileFilter
from .models import Post, Comment
from django.db.models import Q
from .forms import PostForm, CommentForm


class NewsList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'home.html'
    context_object_name = 'home'
    paginate_by = 6
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial


class NewsDetail(FormMixin, DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    form_class = CommentForm
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        pk = self.kwargs.get('pk')
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        try:
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.post = self.get_object()
            self.object.save()
            return super().form_valid(form)
        except IntegrityError:
            return redirect('/')

    def get_success_url(self, **kwargs):
        return reverse_lazy('news', kwargs={'pk': self.get_object().id})


class Search(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        results = ""
        if query:
            results = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'search.html', context={
            'title': 'Поиск',
            'results': page_obj,
            'count': paginator.count
        })


class NewsAdd(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial


class NewsDelete(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/'


class NewsUpgrade(LoginRequiredMixin, UpdateView):
    template_name = 'add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class UserView(ListView):
    model = Post
    template_name = 'users/profile.html'
    context_object_name = 'profile'
    queryset = Comment.objects.order_by('-comment_data')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProfileFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial


class Accept(UpdateView):
    model = Comment
    template_name = 'accept.html'
    form_class = CommentForm
    context_object_name = 'accept'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Вы приняли отклик!'
        id = self.kwargs.get('pk')
        Comment.objects.filter(pk=id).update(accepted=True)
        user = self.object.user
        send_mail(
            subject='Ваш отклик опубликован!',
            message=f'Пользователь опубликовал Ваш отклик.',
            from_email='yamargoshka@inbox.ru',
            recipient_list=[User.objects.filter(username=user).values("email")[0]['email']]
        )
        return context


class Cans(UpdateView):
    model = Comment
    template_name = 'accept.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Вы отменили отклик!'
        id = self.kwargs.get('pk')
        Comment.objects.filter(pk=id).update(accepted=False)
        return context
