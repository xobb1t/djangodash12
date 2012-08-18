from blogs.utils import api_resource

from django import forms
from django.conf import settings


class BlogForm(forms.Form):

    blog = forms.ChoiceField(choices=())

    def __init__(self, token, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        choices = ((None, 'Select your blog'),)
        blogs_data = api_resource(
            settings.BLOGGER_API_ROOT,
            'users/self/blogs',
            token
        )
        if blogs_data:
            for blog in blogs_data['items']:
                choices+=((blog['id'], blog['name']),)
        self.fields['blog'].choices = choices
