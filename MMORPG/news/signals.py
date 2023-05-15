from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Comment
from django.core.mail import send_mail
from django.contrib.auth.models import User


@receiver(post_save, sender=Comment)
def send_mail_resp(sender, instance, created, **kwargs):
    if created:
        user = Post.objects.get(pk=instance.post_id).user
        send_mail(
            subject='Новый отклик',
            message=f'{instance.user} оставил отклик на Ваше объявление: {instance.text}',
            from_email='yamargoshka@inbox.ru',
            recipient_list=[User.objects.filter(username=user).values("email")[0]['email']],
        )
