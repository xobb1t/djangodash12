from django import forms

from .models import Repo


class RepoForm(forms.ModelForm):

    class Meta:
        model = Repo
        fields = ('name', 'cname',)
