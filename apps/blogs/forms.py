from blogs.utils import api_resource

from django import forms
from django.conf import settings

from .models import Blog


class BlogForm(forms.Form):

    blog = forms.ChoiceField(choices=())

    def __init__(self, blog_source=None, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.blog_source = blog_source
        if not self.blog_source:
            return
        choices = ((None, 'Select your blog'),)
        blogs_data = api_resource(
            settings.BLOGGER_API_ROOT,
            'users/self/blogs',
            self.blog_source.access_token
        )
        if not blogs_data:
            return
        for blog in blogs_data['items']:
            choices += ((blog['id'], blog['name']),)
        self.fields['blog'].choices = choices

    def save(self):
        blog_id = self.cleaned_data.get('blog')
        blog_data = api_resource(
            settings.BLOGGER_API_ROOT,
            'blogs/{0}'.format(blog_id),
            self.blog_source.access_token
        )
        if blog_data:
            domain = blog_data['url'].lower().replace('/', '')
            domain = domain.replace('http:', '')
            title = blog_data['name']
            blog = Blog.objects.create(
                source=self.blog_source,
                identificator=blog_id,
                domain=domain,
                title=title,
            )
            return blog
        return None
