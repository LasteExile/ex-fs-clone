from django.db import models
from django.urls import reverse_lazy


class MotionPicture(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    url = models.SlugField(max_length=200, unique=True)
    type = models.PositiveSmallIntegerField(
        choices=(
            (0, 'movie'),
            (1, 'series'),
            (2, 'show')
        ))
    released = models.DateField(null=True, blank=True)
    iframe_src = models.CharField(max_length=200)
    plot = models.TextField()
    poster_url = models.CharField(max_length=300, null=True, blank=True)
    languages = models.ManyToManyField('Language')
    genres = models.ManyToManyField('Genre')
    memberships = models.ManyToManyField('Membership')

    def __str__(self):
        return f'{self.title} : {self.url}'

    def get_absolute_url(self):
        return reverse_lazy('details', args=[str(self.url)])
    

class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Membership(models.Model):
    name = models.CharField(max_length=200)
    career = models.ManyToManyField('Career')
    poster = models.ImageField(upload_to='actors/', null=True, blank=True)

    def __str__(self):
        return self.name


class Career(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Rating(models.Model):
    motion_picture = models.ForeignKey('MotionPicture', on_delete=models.CASCADE, related_name='motion_picture',
                                       null=True, blank=True)
    name = models.ManyToManyField('RatingName')
    value = models.FloatField()
    max_value = models.FloatField()

    def __str__(self):
        return self.motion_picture.title


class RatingName(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
