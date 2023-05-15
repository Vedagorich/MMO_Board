import datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Post


@shared_task
def celery_week_mails():
    time_delta = datetime.timedelta(7)
    start_date = datetime.datetime.utcnow() - time_delta
    end_date = datetime.datetime.utcnow()

    posts = Post.objects.filter(created_at__range=(start_date, end_date))
    users = User.objects.all()
    users_emails = [user.email for user in users]
    html_content = render_to_string('account/email/week_email.html',
                                        {'posts': posts,}, )
    msg = EmailMultiAlternatives(
        subject=f'"Еженедельная подписка (celery)"',
        body="Новости",
        from_email='yamargoshka@inbox.ru',
        to=users_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
