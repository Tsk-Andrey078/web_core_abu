from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Navigation, Widget, Content, NewsContent, OtherContent, NavigationHistory, WidgetHistory, Questionaire

class NavigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Navigation
        fields = [
            "id",
            "title",
            "slug",
            "order",
            "language_key",
            "navigation_id",
            "navigation_type",
            "create_date",
            "update_date",
        ]

class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = [
            "id",
            "widget_type",
            "options",
            "language_key",
            "order",
            "navigation_id",
        ]

class OtherContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherContent
        fields = [
            'content',
        ]

class NewsContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsContent
        fields = [
            "id",
            "image",
            "title",
            "content",
        ]

class PolymorphicChildSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if isinstance(instance, OtherContent):
            return OtherContentSerializer(instance).data
        elif isinstance(instance, NewsContent):
            return NewsContentSerializer(instance).data
        return super().to_representation(instance)

class WidgetChildrenSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Widget
        fields = [
            "id",
            "widget_type",
            "options",
            "language_key",
            "order",
            "navigation_id",
            "children",
        ]

    def get_children(self, obj):
        content_ids = Content.objects.filter(widget_id=obj.id)
        content_other = []
        content_news = []
        for content in content_ids:
            if content.content_group == "Other":
                content_other.append(OtherContent.objects.only('id', 'content').get(id=content.content_id))
            if content.content_group == "News":
                print(NewsContent.objects.get(id=content.content_id))
                content_news.append(NewsContent.objects.only('id', 'title', 'image', 'content').get(id=content.content_id))
        children = list(content_other) + list(content_news)
        return PolymorphicChildSerializer(children, many=True).data
    
class NavigationChildrenSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Navigation
        fields = [
            "id",
            "title",
            "slug",
            "order",
            "language_key",
            "navigation_id",
            "navigation_type",
            "create_date",
            "update_date",
            "children",
        ]

    def get_children(self, obj):
        children = Navigation.objects.filter(navigation_id=obj.id)
        if children.exists():
            return NavigationChildrenSerializer(children, many=True).data
        return []
    
class NavigationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NavigationHistory
        fields = [
            "idn",
            "title",
            "slug",
            "order",
            "language_key",
            "navigation_id",
            "navigation_type",
            "change_type",
            "create_date",
        ]

class WidgetHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WidgetHistory
        fields = [
            "idn",
            "widget_type",
            "options",
            "language_key",
            "order",
            "navigation_id",
            "create_date",
        ]