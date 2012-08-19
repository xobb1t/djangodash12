Date: {{ post.published }}
Title: {{ post.title }}{% if post.labels %}
Tags: {% for label in post.label %}{{ label }}{% if not forloop.last %}, {% endif %}{% endfor %}{% endif %}
Slug: {{ slug }}

{{ post.content|safe }}
