from django.views.generic import TemplateView, FormView, DetailView, DeleteView, ListView
from django.http import HttpResponseRedirect

from . import models, forms, get_data


class MotionPictureListView(ListView):
    model = models.MotionPicture
    template_name = 'motion_pictures/motionpictures.html'
    paginate_by = 20

    def get_queryset(self):
        genre = models.Genre.objects.get(pk=self.request.GET.get('genre'))
        queryset = models.MotionPicture.objects.filter(genres=genre)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = models.Genre.objects.get(pk=self.request.GET.get('genre'))
        return context


class IndexListView(ListView):
    model = models.MotionPicture
    template_name = 'motion_pictures/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        film_list = []
        series_list = []
        films = models.MotionPicture.objects.filter(type=0).order_by('-pub_date')[:8]
        series = models.MotionPicture.objects.filter(type=1).order_by('-pub_date')[:8]

        for i in films:
            genres = ''
            if i.genres.count() > 3:
                genres = f'{i.genres.all()[0].name}, {i.genres.all()[1].name}, {i.genres.all()[2].name}...'
            elif i.genres.count() == 1:
                genres = f'{i.genres.all()[0].name}'
            elif i.genres.count() == 0:
                genres = 'None'
            else:
                for j in range(i.genres.count() - 1):
                    genres += f'{i.genres.all()[j].name}, '
                genres += f'{i.genres.all()[i.genres.count() - 1].name}'
            film_list.append([i, genres])

        for i in series:
            genres = ''
            if i.genres.count() > 3:
                genres = f'{i.genres.all()[0].name}, {i.genres.all()[1].name}, {i.genres.all()[2].name}...'
            elif i.genres.count() == 1:
                genres = f'{i.genres.all()[0].name}'
            elif i.genres.count() == 0:
                genres = 'None'
            else:
                for j in range(i.genres.count() - 1):
                    genres += f'{i.genres.all()[j].name}, '
                genres += f'{i.genres.all()[i.genres.count() - 1].name}'
            series_list.append([i, genres])

        context['film_list'] = film_list
        context['series_list'] = series_list
        context['genre_list'] = models.Genre.objects.all()
        return context


class MotionPicturesSearchView(ListView):
    model = models.MotionPicture
    template_name = 'motion_pictures/search.html'
    paginate_by = 20

    def get_queryset(self):
        name = self.request.GET.get('search')
        queryset = models.MotionPicture.objects.filter(title__icontains=name)
        return queryset


class FilmListView(ListView):
    model = models.MotionPicture
    template_name = 'motion_pictures/films.html'
    paginate_by = 20
    queryset = models.MotionPicture.objects.filter(type=0).order_by('-pub_date')


class SeriesListView(ListView):
    model = models.MotionPicture
    template_name = 'motion_pictures/series.html'
    paginate_by = 20
    queryset = models.MotionPicture.objects.filter(type=1).order_by('-pub_date')


class MotionPictureDetailView(DetailView):
    model = models.MotionPicture
    slug_field = 'url'
    template_name = 'motion_pictures/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actors'] = models.Membership.objects.filter(motionpicture=context['motionpicture'], career__name='Actor')
        context['writers'] = models.Membership.objects.filter(motionpicture=context['motionpicture'], career__name='Writer')
        context['directors'] = models.Membership.objects.filter(motionpicture=context['motionpicture'], career__name='Director')
        context['genres'] = models.Genre.objects.filter(motionpicture=context['motionpicture'])
        context['languages'] = models.Language.objects.filter(motionpicture=context['motionpicture'])
        rating_list = []
        ratings = models.Rating.objects.filter(motion_picture=context['motionpicture'])
        for i in ratings:
            rating_list.append([i, models.RatingName.objects.filter(rating=i)])
        context['ratings'] = rating_list
        return context


class MotionPictureAddView(FormView):
    form_class = forms.AddMotionPictureForm
    template_name = 'motion_pictures/add.html'

    def form_valid(self, form):
        type = {'movie': 0, 'series': 1, 'show': 2}
        data = get_data.get_data(self.request.POST.get('imdb_link'))[1]
        motion_picture = models.MotionPicture.objects.create(
            title=data.get('title'),
            url=data.get('id'),
            type=type.get(data.get('type')),
            released=data.get('released'),
            iframe_src=data.get('iframe_src'),
            plot=data.get('plot'),
            poster_url=data.get('poster')
        )
        motion_picture.save()
        genres = []
        languages = []

        for i in data.get('actors'):
            if i != 'N/A':
                try:
                    actor = models.Membership.objects.get(name=i)
                except:
                    actor = models.Membership.objects.create(name=i)
                    actor.career.add(models.Career.objects.get(name='Actor'))
                    actor.save()
                motion_picture.memberships.add(actor)

        for i in data.get('directors'):
            if i != 'N/A':
                try:
                    director = models.Membership.objects.get(name=i)
                except:
                    director = models.Membership.objects.create(name=i)
                    director.career.add(models.Career.objects.get(name='Director'))
                    director.save()
                motion_picture.memberships.add(director)

        for i in data.get('writers'):
            if i != 'N/A':
                try:
                    writer = models.Membership.objects.get(name=i)
                except:
                    writer = models.Membership.objects.create(name=i)
                    writer.career.add(models.Career.objects.get(name='Writer'))
                    writer.save()
                motion_picture.memberships.add(writer)

        for i in data.get('genres'):
            try:
                genre = models.Genre.objects.get(name=i)
            except:
                genre = models.Genre.objects.create(name=i)
                genre.save()
            genres.append(genre)

        for i in data.get('ratings'):
            try:
                rating_name = models.RatingName.objects.get(name=i.get('source'))
            except:
                rating_name = models.RatingName.objects.create(name=i.get('source'))
                rating_name.save()
            if '%' in i.get('value'):
                value = i.get('value')[:-1]
                max_value = 100
            else:
                value, max_value = map(float, i.get('value').split('/'))
            rating = models.Rating.objects.create(motion_picture=motion_picture, value=value, max_value=max_value)
            rating.name.add(rating_name)
            rating.save()

        for i in data.get('languages'):
            try:
                language = models.Language.objects.get(name=i)
            except:
                language = models.Language.objects.create(name=i)
                language.save()
            languages.append(language)

        motion_picture.genres.set(genres)
        motion_picture.languages.set(languages)
        motion_picture.save()
        return HttpResponseRedirect(motion_picture.get_absolute_url())
