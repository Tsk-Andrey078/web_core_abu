from django.contrib import admin
from .models import (
    Navigation, Widget, Content, NewsContent, 
    OtherContent, NavigationHistory, WidgetHistory, 
    Questionaire
)

class NavigationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'order', 'language_key', 'navigation_id', 'navigation_type')
    search_fields = ('title', 'slug', 'language_key')
    
class WidgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'widget_type', 'options', 'language_key', 'order', 'navigation_id')
    search_fields = ('widget_type', 'options', 'language_key')

models = [
    (Navigation, NavigationAdmin),
    (Widget, WidgetAdmin),
    (Content, admin.ModelAdmin),
    (NewsContent, admin.ModelAdmin),
    (OtherContent, admin.ModelAdmin),
    (NavigationHistory, admin.ModelAdmin),
    (WidgetHistory, admin.ModelAdmin),
    (Questionaire, admin.ModelAdmin),
]

for model, admin_class in models:
    admin.site.register(model, admin_class)