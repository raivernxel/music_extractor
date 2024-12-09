from django import forms

class SongForm(forms.Form):
    track_name = forms.CharField(label='Enter song name', max_length=200)
