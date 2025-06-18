from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    location = models.CharField(max_length=30, blank=True, verbose_name='Местоположение')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')

    def __str__(self):
        return f'Профиль {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    #Service
class ServicePackage(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название пакета')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    duration = models.CharField(max_length=50, verbose_name='Длительность')
    is_popular = models.BooleanField(default=False, verbose_name='Популярный пакет')
    image = models.ImageField(upload_to='services/', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пакет услуг'
        verbose_name_plural = 'Пакеты услуг'