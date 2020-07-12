from .models import Video
from django import forms
class VideoForm(forms.ModelForm):
    class Meta:
        model  = Video
        fields = ['url']
        labels = {'url':'YouTube URL'}
class Search(forms.Form):
    search = forms.CharField(max_length = 350,label = 'Search For Videos')
