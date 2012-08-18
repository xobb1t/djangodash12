from django import forms

from .models import Repo
from .utils import repo_exists


class RepoForm(forms.ModelForm):

    class Meta:
        model = Repo
        fields = ('name', 'cname',)

    def __init__(self, repo_user=None, *args, **kwargs):
        self.repo_user = repo_user
        super(RepoForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        access_token = self.repo_user.access_token
        login = self.repo_user.username
        repo = self.cleaned_data['name']
        if repo_exists(access_token, login, repo):
            raise forms.ValidationError('{0} exists!'.format(repo))
        return repo
