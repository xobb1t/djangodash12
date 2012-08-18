from blogs.utils import api_resource

from django import forms
from django.conf import settings

from .models import Blog


class BlogForm(forms.Form):

    blog = forms.ChoiceField(choices=())

    def __init__(self, blog_source, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.blog_source = blog_source
        choices = ((None, 'Select your blog'),)
        blogs_data = api_resource(
            settings.BLOGGER_API_ROOT,
            'users/self/blogs',
            blog_source.access_token
        )
        if blogs_data:
            for blog in blogs_data['items']:
                choices+=((blog['id'], blog['name']),)
        self.fields['blog'].choices = choices

    def save(self):
        blog_id = self.cleaned_data.get('blog')
        blog_data = api_resource(
            settings.BLOGGER_API_ROOT,
            'blogs/{0}'.format(blog_id),
            self.blog_source.access_token
        )
        if blog_data:
            blog = Blog.objects.create(
                source=self.blog_source, identificator=blog_id,
                domain=blog_data['url']
            )
            return blog
        return None
