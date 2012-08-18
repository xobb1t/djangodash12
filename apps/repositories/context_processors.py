from django.conf import settings
from django.utils.functional import SimpleLazyObject


def github_auth_url(request):
    def get_github_auth_url():
        return '{0}{1}?response_type=token&client_id={2}&redirect_uri'\
               '={3}&scope={4}'.format(settings.GITHUB_AUTH_HOST,
                    settings.GITHUB_AUTH_PATH, settings.GITHUB_ID,
                    settings.GITHUB_CALLBACK_URL,
                    ','.join(settings.GITHUB_SCOPES)
                )
    return {'github_auth_url': SimpleLazyObject(get_github_auth_url)}
