from django import forms

from . import get_data, models


class AddMotionPictureForm(forms.Form):
    imdb_link = forms.CharField(label='IMDB link')

    def clean_imdb_link(self):
        link = self.cleaned_data['imdb_link']
        data = get_data.get_data(link)
        if not data[0]:
            self.add_error('imdb_link', data[1])
        try:
            models.MotionPicture.objects.get(url=data[1].get('id'))
            self.add_error('imdb_link', 'Motion Picture with this link already exist')
        except:
            pass
