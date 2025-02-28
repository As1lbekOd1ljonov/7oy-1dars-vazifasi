from django.contrib import admin
from .models import Brands, Color, Cars, Comment


class Brandsadmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
admin.site.register(Brands, Brandsadmin)


class Carsadmin(admin.ModelAdmin):
    list_display = ('car_name', 'brand', 'date' , 'color')
    list_display_links = ('car_name', )
    search_fields = ('car_name', 'brand')
    list_max_show_all = 10
    list_per_page = 10
admin.site.register(Cars, Carsadmin)



class Coloradmin(admin.ModelAdmin):
    list_display = ('color',)
    list_display_links = ('color',)
    search_fields = ('color',)
    list_max_show_all = 10
    list_per_page = 10
admin.site.register(Color, Coloradmin)


class Commentadmin(admin.ModelAdmin):
    list_display = ('text',)
    list_display_links = ('text',)
admin.site.register(Comment, Commentadmin)