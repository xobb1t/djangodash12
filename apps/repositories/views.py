from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

from .models import User
from .utils import get_access_data, get_user_info


def oauth2callback(request):
    if not request.GET.get('code', None):
        raise Http404

    access_data = get_access_data(request.GET.get('code'))
    access_token = access_data.get('access_token', None)
    if not access_token:
        messages.error(request, 'Did not receive access token!')
        return HttpResponseRedirect(reverse('home'))

    identification, username = get_user_info(access_token)
    if not identification or not username:
        messages.error(request, 'Did not receive user info!')
        return HttpResponseRedirect(reverse('home'))

    user_obj, created = User.objects.get_or_create(
        identification=identification,
        defaults={
            'access_token': access_token,
            'username' username
        }
    )
    if not created:
        user_obj.access_token = access_token
        user_obj.username = username
        user_obj.save()

    request.session['repositories_user'] = user_obj
    request.session.modified = True
    return HttpResponseRedirect(reverse('home'))
