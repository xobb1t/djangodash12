from django import forms

from .models import Repo
from .utils import repo_exists


class RepoForm(forms.ModelForm):

    class Meta:
        model = Repo
        fields = ('name', 'cname',)

    def __init__(self, repositories_user=None, *args, **kwargs):
        self.repositories_user = repositories_user
        super(RepoForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        access_token = self.repositories_user.access_token
        login = self.repositories_user.username
        repo = self.cleaned_data['name']
        if repo_exists(access_token, login, repo):
            raise forms.ValidationError('{0} exists!'.format(repo))
        return repo
