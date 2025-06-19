from django.db import models

class Contact(models.Model):
    club_name = models.CharField(max_length=100, verbose_name='Название клуба')
    address = models.TextField(verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    opening_hours = models.TextField(verbose_name='Часы работы')
    map_embed_code = models.TextField(
        verbose_name='Код карты (iframe)',
        help_text='Код для встраивания карты из Google/Yandex Maps'
    )
    social_facebook = models.URLField(blank=True, verbose_name='Facebook')
    social_vk = models.URLField(blank=True, verbose_name='ВКонтакте')
    social_telegram = models.URLField(blank=True, verbose_name='Telegram')
    social_instagram = models.URLField(blank=True, verbose_name='Instagram')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.club_name