from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.MotionPictureAddView.as_view(), name='add'),
    path('details/<slug>', views.MotionPictureDetailView.as_view(), name='details'),
    path('films/', views.FilmListView.as_view(), name='films'),
    path('series/', views.SeriesListView.as_view(), name='series'),
    path('genre/', views.MotionPictureListView.as_view(), name='motionpictures'),
    path('search_result/', views.MotionPicturesSearchView.as_view(), name='search'),
    path('', views.IndexListView.as_view(), name='index')
]