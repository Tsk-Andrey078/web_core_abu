from django.contrib import admin
from .models import Navigation, Widget, Content, NewsContent, OtherContent, NavigationHistory, WidgetHistory, Questionaire
# Register your models here.
admin.site.register(Navigation)
admin.site.register(Widget)
admin.site.register(Content)
admin.site.register(NewsContent)
admin.site.register(OtherContent)
admin.site.register(NavigationHistory)
admin.site.register(WidgetHistory)
admin.site.register(Questionaire)