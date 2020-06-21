from django.contrib import admin

from . import models


admin.site.register(models.MotionPicture)
admin.site.register(models.Membership)
admin.site.register(models.Career)
admin.site.register(models.Genre)
admin.site.register(models.Rating)
admin.site.register(models.RatingName)
admin.site.register(models.Language)


