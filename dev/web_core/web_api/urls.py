from django.urls import path, include
from .views import NavigationView, WidgetChildrenView, NavigationWidgetsView, NavigationChildrenView, WidgetView, FileUploadView, NavigationChildrenAllView, GetNavigationHistory, GetWidgetHistory
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
    path('navigation-history', GetNavigationHistory.as_view(), name="navigation-history"),
    path('widget-history', GetWidgetHistory.as_view(), name="widget-history"),
    path('token/', obtain_auth_token, name='obtain_token'),
    path('', include(router.urls)),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
]
