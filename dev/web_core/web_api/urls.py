from django.urls import path, include
from .views import NavigationView, WidgetChildrenView, NavigationWidgetsView, NavigationChildrenView, WidgetView, FileUploadView, NavigationChildrenAllView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('navigation-view', NavigationView, basename='navigation-view')
router.register('widget-view', WidgetView, basename='widget-view')

urlpatterns = [
    path('widget-children/<int:id>', WidgetChildrenView.as_view(), name="widget_children"),
    path('widget/navigation/<int:id>', NavigationWidgetsView.as_view(), name="navigation_widgets"),
    path('navigation/<int:id>/children', NavigationChildrenView.as_view(), name="navigation-children"),
    path('navigation-children-all', NavigationChildrenAllView.as_view(), name="navigation-children-all"),
    path('', include(router.urls)),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
]
