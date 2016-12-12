from django.conf.urls import url, patterns, include

urlpatterns = patterns('',
	url(r'^', include('otree.default_urls')),	
    url(r'^s3direct/', include('s3direct.urls')),
)
