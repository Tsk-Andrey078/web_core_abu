from django.db import models

# Create your models here.
class Navigation(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=128)
    order = models.IntegerField()
    language_key = models.CharField(max_length=64)
    navigation_id = models.IntegerField(default=None, blank=True, null=True)
    navigation_type = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Widget(models.Model):
    id = models.AutoField(primary_key=True)
    widget_type = models.CharField(max_length=255)
    options = models.JSONField()
    language_key = models.CharField(max_length=64)
    order = models.IntegerField()
    navigation_id = models.ForeignKey(Navigation, related_name='widgets', to_field='id', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
    
class Content(models.Model):
    id = models.AutoField(primary_key=True)
    widget_id = models.IntegerField()
    content_id = models.IntegerField()
    language_key = models.CharField(max_length=64)
    content_group = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.id}"

class NewsContent(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    image = models.TextField()
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"

class OtherContent(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.JSONField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
    
class NavigationHistory(models.Model):
    idn = models.IntegerField()
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=128)
    order = models.IntegerField()
    language_key = models.CharField(max_length=64)
    navigation_id = models.IntegerField(default=None, blank=True, null=True)
    navigation_type = models.CharField(max_length=255)
    change_type = models.CharField(max_length=128)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class WidgetHistory(models.Model):
    idn = models.IntegerField()
    widget_type = models.CharField(max_length=255)
    options = models.JSONField()
    language_key = models.CharField(max_length=64)
    order = models.IntegerField()
    navigation_id = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
    
class Questionaire(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=512)
    dob = models.DateField()
    phone = models.CharField(max_length=128)
    place = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    graduate = models.CharField(max_length=255)
    speciality = models.CharField(max_length=128)
    qualification_category = models.CharField(max_length=128)
    place_of_work = models.TextField()
    job = models.CharField(max_length=128)
    teaching_experience = models.IntegerField()
    experience_by_position = models.CharField(max_length=128)

    def __str__(self):
        return self.full_name