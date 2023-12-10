from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import PostCategory
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
def send_notify(preview,pk,title,subcribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text':preview,
            'link': f'http://127.0.0.1:8000/posts/{pk}',
        }


    )
    msg = EmailMultiAlternatives(subject=title,body='',from_email='for.skillfactory@yandex.ru',to=subcribers)
    msg.attach_alternative(html_content,'text/html')
    msg.send()



@receiver(m2m_changed,sender=PostCategory)
def notify_post(sender,instance,**kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribe_emails = []

        for item in categories:
            subscribe = item.subscribe.all()
            subscribe_emails += [s.email for s in subscribe]

        send_notify(instance.preview(),instance.pk,instance.title,subscribe_emails)

@receiver(post_save, sender=User)
def welcome_email(created, **kwargs):
    instance = kwargs['instance']
    if created:
        html_content = render_to_string(
            'welcome.html',
            {
                'text': f'{instance.username}, Ваша регистрация прошла успешно!',
            }
        )
        msg = EmailMultiAlternatives(
            subject='Добро пожаловать!',
            body='',
            from_email='for.skillfactory@yandex.ru',
            to=[instance.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()