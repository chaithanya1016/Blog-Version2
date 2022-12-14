from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.cache import cache


@receiver(user_logged_in, sender=User)
def login_sucess(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    request.session['ip'] = ip




@receiver(user_logged_in, sender=User)
def login_success(sender, request, user, **kwargs):
    ct = cache.get('count', 0, version=user.pk)
    newcount = ct + 1
    cache.set('count', newcount, 60*60*48, version=user.pk)
    print(user.pk)


