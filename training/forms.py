from django import forms
from s3direct.widgets import S3DirectWidget

class ImageForm(forms.Form):
	image = forms.URLField(widget=S3DirectWidget(dest='imgs'))
	
