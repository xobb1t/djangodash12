from django.conf.urls import patterns, url


urlpatterns = patterns(
    'parser.views',
    url(r'^start/$', 'start_import', name='start_import'),
    url(r'^results/$', 'results', name='parser_results'),
)
