from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

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

# Бронирование

class Computer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    specs = models.TextField(verbose_name='Характеристики', blank=True)
    
    def __str__(self):
        return f"Компьютер #{self.id} - {self.name}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE, verbose_name='Компьютер')
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Ожидает'),
            ('confirmed', 'Подтверждено'),
            ('canceled', 'Отменено'),
            ('completed', 'Завершено')
        ],
        default='pending',
        verbose_name='Статус'
    )
    
    class Meta:
        ordering = ['start_time']
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
    
    def __str__(self):
        return f"Бронирование #{self.id} - {self.computer} ({self.start_time} - {self.end_time})"
    
    @property
    def duration_hours(self):
        duration = self.end_time - self.start_time
        return round(duration.total_seconds() / 3600)
    
    @property
    def can_be_canceled(self):
        return (self.start_time > timezone.now() and 
                self.status in ['pending', 'confirmed'])
    
    # Tournament

class Tournament(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название турнира')
    game = models.CharField(max_length=100, verbose_name='Игра')
    description = models.TextField(verbose_name='Описание')
    start_date = models.DateTimeField(verbose_name='Дата и время начала')
    end_date = models.DateTimeField(verbose_name='Дата и время окончания')
    max_participants = models.PositiveIntegerField(verbose_name='Максимум участников')
    prize_pool = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Призовой фонд')
    rules = models.TextField(verbose_name='Правила турнира')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.game})"

    @property
    def status(self):
        now = timezone.now()
        if now < self.start_date:
            return 'upcoming'
        elif self.start_date <= now <= self.end_date:
            return 'ongoing'
        else:
            return 'finished'

    @property
    def registered_count(self):
        return self.participants.count()

    class Meta:
        ordering = ['start_date']
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'

class TournamentRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tournament_registrations')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='participants')
    registration_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'tournament')
        verbose_name = 'Регистрация на турнир'
        verbose_name_plural = 'Регистрации на турниры'

    def __str__(self):
        return f"{self.user.username} - {self.tournament.name}"