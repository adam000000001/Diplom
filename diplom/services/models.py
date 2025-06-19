from django.db import models
from django.contrib.auth.models import User

class Platform(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название платформы')
    icon = models.CharField(max_length=50, help_text='Имя класса иконки (например, "fa-desktop" для Font Awesome)')
    
    def __str__(self):
        return self.name

class ServicePackage(models.Model):
    DURATION_CHOICES = [
        (30, '30 минут'),
        (60, '1 час'),
        (120, '2 часа'),
        (180, '3 часа'),
        (240, '4 часа'),
        (300, '5 часов'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Название пакета')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    duration = models.PositiveIntegerField(choices=DURATION_CHOICES, verbose_name='Длительность')
    platforms = models.ManyToManyField(Platform, verbose_name='Доступные платформы')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_popular = models.BooleanField(default=False, verbose_name='Популярный')
    
    def __str__(self):
        return f"{self.name} - {self.get_duration_display()}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('canceled', 'Отменен'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    package = models.ForeignKey(ServicePackage, on_delete=models.PROTECT, verbose_name='Пакет')
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT, verbose_name='Платформа')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    payment_id = models.CharField(max_length=100, blank=True, verbose_name='ID платежа')
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.package.name}"