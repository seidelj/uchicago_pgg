from django.conf.urls import url

urlpatterns = patterns('',
	url(r'^s3direct/', include('s3direct.urls')),
)
