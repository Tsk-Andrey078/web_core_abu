import os
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Navigation, Widget, Content, NewsContent, OtherContent, NavigationHistory, WidgetHistory, Questionaire
from .serializer import NavigationSerializer, WidgetSerializer, WidgetChildrenSerializer, NavigationChildrenSerializer, NavigationHistorySerializer, WidgetHistorySerializer
from datetime import datetime

#Вьюсет на модель Navigation. При использовании метода patch или delete изменения отправляются в NavigationHistory.
#В случае если у Navigation имеются дети среди navigation у которых navigation_id = id удаляемого родите, они также рекурсивно удаляются.
class NavigationView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Navigation.objects.all()
    serializer_class = NavigationSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Navigation.objects.all()
        navigation_type = self.request.query_params.get('navigation_type', None)
        if navigation_type:
            queryset = queryset.filter(navigation_type=navigation_type)
        slug = self.request.query_params.get('slug', None)
        if slug:
            language_key = self.request.query_params.get('language_key', None)
            queryset = queryset.filter(language_key=language_key, slug=slug)
        return queryset

    def get_permissions(self):
        # Если запрос на получение списка, использовать AllowAny
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instanse = self.get_object()
    
        NavigationHistory.objects.create(
            idn = instanse.id,
            title = instanse.title,
            slug = instanse.slug,
            order = instanse.order,
            language_key = instanse.language_key,
            navigation_id = instanse.navigation_id,
            navigation_type = instanse.navigation_type,
            change_type = request.query_params.get('change_type'),
        )

        serializer = self.get_serializer(instanse, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instanse = kwargs.get('instanse', None) or self.get_object()

        NavigationHistory.objects.create(
            idn = instanse.id,
            title = instanse.title,
            slug = instanse.slug,
            order = instanse.order,
            language_key = instanse.language_key,
            navigation_id = instanse.navigation_id,
            navigation_type = instanse.navigation_type,
            change_type = request.query_params.get('change_type'),
        )

        widgets = Widget.objects.filter(navigation_id=instanse.id)
        for widget in widgets:
            WidgetHistory.objects.create(
                idn = widget.id,
                widget_type = widget.widget_type,
                options = widget.options,
                language_key = widget.language_key,
                order = widget.order,
                navigation_id = instanse.id,
            )

        children = Navigation.objects.filter(navigation_id=instanse.id)
        for child in children:
            self.destroy(request, instanse=child)

        self.perform_destroy(instanse)
        return Response(status = status.HTTP_204_NO_CONTENT)
    
    def perform_derstroy(self, instanse):
        instanse.delete()

#Вывод Navigations с детьми из рядов navigations. Работает рекурсивно и предполагает любой уровень вложенностей.
class NavigationChildrenAllView(APIView):
    serializer_class = NavigationChildrenSerializer

    def get(self, request, *args, **kwargs):
        try:
            language_key = request.query_params.get("language_key", None)
            if language_key:
                data = Navigation.objects.filter(navigation_id__isnull=True, language_key=language_key).exclude(navigation_type='template')
            else:            
                data = Navigation.objects.filter(navigation_id__isnull=True).exclude(navigation_type='template')
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

#Вывод детей Navigation у которых navigation_id = id родителя
class NavigationChildrenView(APIView):
    serializer_class = NavigationSerializer
    
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs: 
            try:
                data = Navigation.objects.filter(navigation_id=kwargs['id'])
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data)

#Вьюсет на модель Widget. При использовании метода patch или delete изменения отправляются в WidgetHistory
class WidgetView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Widget.objects.all()
        language_key = self.request.query_params.get('language_key', None)
        if language_key:
            queryset = Widget.objects.filter(language_key=language_key)
        return queryset
    
    def get_permissions(self):
        # Если запрос на получение списка, использовать AllowAny
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instanse = self.get_object()
    
        WidgetHistory.objects.create(
            idn = instanse.id,
            widget_type = instanse.widget_type,
            options = instanse.options,
            language_key = instanse.language_key,
            order = instanse.order,
            navigation_id = request.query_params.get('navigation_id'),
        )

        serializer = self.get_serializer(instanse, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instanse = self.get_object()

        WidgetHistory.objects.create(
            idn = instanse.id,
            widget_type = instanse.widget_type,
            options = instanse.options,
            language_key = instanse.language_key,
            order = instanse.order,
            navigation_id = request.query_params.get('navigation_id'),
        )

        self.perform_destroy(instanse)
        return Response(status = status.HTTP_204_NO_CONTENT)

    def perform_derstroy(self, instanse):
        instanse.delete()
    
#Вывод Widget с доечерними элементами, а именно с контентом
class WidgetChildrenView(APIView):
    serializer_class = WidgetChildrenSerializer

    def get(self, request, *args, **kwargs):
        data = Widget.objects.get(id=kwargs['id'], language_key=request.query_params.get('language_key'))
        return Response(self.serializer_class(data).data)

#Вывод Widgets определенного Navigation    
class NavigationWidgetsView(APIView):
    serializer_class = WidgetChildrenSerializer

    def get(self, request, *args, **kwargs):
        data = Widget.objects.filter(navigation_id=kwargs['id'], language_key=request.query_params.get('language_key'))
        return Response(self.serializer_class(data, many=True).data)

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if file_obj:
            # Генерация уникального имени файла
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            file_extension = os.path.splitext(file_obj.name)[1]
            new_file_name = f"{current_time}{file_extension}"

            # Сохранение файла на файловую систему
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', new_file_name)
            file_name = default_storage.save(file_path, file_obj)
            return Response({"message": "Файл загружен успешно", "file_name": file_name}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Файл не найден"}, status=status.HTTP_400_BAD_REQUEST)
        
class GetNavigationHistory(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NavigationHistorySerializer

    def get(self, request, *args, **kwargs):
        idn = request.query_params.get('id', None)
        if idn:
            data = NavigationHistory.objects.filter(idn=idn)
            return Response(self.serializer_class(data, many=True).data)
        
        ruidn = request.query_params.get('ruidn')
        kzidn = request.query_params.get('kzidn')

        # Получение данных из таблицы NavigationHistory
        history_ru = NavigationHistory.objects.filter(idn=ruidn).order_by('create_date')
        history_kz = NavigationHistory.objects.filter(idn=kzidn).order_by('create_date')

        if not history_ru.exists() or not history_kz.exists():
            return Response({"error": "No data found for the provided ruidn and kzidn"}, status=status.HTTP_404_NOT_FOUND)

        # Создание пар
        pairs = []
        min_length = min(len(history_ru), len(history_kz))
        for i in range(min_length):
            pairs.append((history_ru[i], history_kz[i]))

        # Добавление оставшихся элементов, если один из списков длиннее
        if len(history_ru) > min_length:
            for i in range(min_length, len(history_ru)):
                pairs.append((history_ru[i], None))
        elif len(history_kz) > min_length:
            for i in range(min_length, len(history_kz)):
                pairs.append((None, history_kz[i]))

        # Сериализация данных
        serialized_pairs = [
            {
                'ru': NavigationHistorySerializer(pair[0]).data if pair[0] else None,
                'kz': NavigationHistorySerializer(pair[1]).data if pair[1] else None
            }
            for pair in pairs
        ]

        return Response(serialized_pairs, status=status.HTTP_200_OK)
        
class GetWidgetHistory(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WidgetHistorySerializer

    def get(self, request, *args, **kwargs):
        idn = request.query_params.get('id', None)
        if idn:
            data = WidgetHistory.objects.filter(idn=idn)
            return Response(self.serializer_class(data, many=True).data)
        
        ruidn = request.query_params.get('ruidn')
        kzidn = request.query_params.get('kzidn')

        if not ruidn or not kzidn:
            return Response({"error": "Both ruidn and kzidn parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Получение данных из таблицы WidgetHistory
        history_ru = WidgetHistory.objects.filter(idn=ruidn).order_by('create_date')
        history_kz = WidgetHistory.objects.filter(idn=kzidn).order_by('create_date')

        if not history_ru.exists() or not history_kz.exists():
            return Response({"error": "No data found for the provided ruidn and kzidn"}, status=status.HTTP_404_NOT_FOUND)

        # Создание пар
        pairs = []
        min_length = min(len(history_ru), len(history_kz))
        for i in range(min_length):
            pairs.append((history_ru[i], history_kz[i]))

        # Добавление оставшихся элементов, если один из списков длиннее
        if len(history_ru) > min_length:
            for i in range(min_length, len(history_ru)):
                pairs.append((history_ru[i], None))
        elif len(history_kz) > min_length:
            for i in range(min_length, len(history_kz)):
                pairs.append((None, history_kz[i]))

        # Сериализация данных
        serialized_pairs = [
            {
                'ru': WidgetHistorySerializer(pair[0]).data if pair[0] else None,
                'kz': WidgetHistorySerializer(pair[1]).data if pair[1] else None
            }
            for pair in pairs
        ]

        return Response(serialized_pairs, status=status.HTTP_200_OK)