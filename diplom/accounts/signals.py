from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Tournament, TournamentRegistration, TournamentNotification
from django.utils import timezone
from datetime import timedelta

@receiver(post_save, sender=TournamentRegistration)
def create_notification(sender, instance, created, **kwargs):
    if created:
        TournamentNotification.objects.create(
            tournament=instance.tournament,
            user=instance.user
        )

def check_tournament_start():
    now = timezone.now()
    upcoming_tournaments = Tournament.objects.filter(
        start_date__gt=now,
        start_date__lte=now + timedelta(hours=24)  # Турниры, которые начнутся в ближайшие 24 часа
    )
    
    for tournament in upcoming_tournaments:
        send_tournament_reminders(tournament)

def send_tournament_reminders(tournament):
    registrations = TournamentRegistration.objects.filter(
        tournament=tournament,
        is_confirmed=True
    )
    
    for registration in registrations:
        # Проверяем, не было ли уже уведомления
        notification, created = TournamentNotification.objects.get_or_create(
            tournament=tournament,
            user=registration.user
        )
        
        if not notification.sent_email:
            send_email_notification(registration.user, tournament)
            notification.sent_email = True
            notification.save()
        
        # Здесь можно добавить браузерные уведомления

def send_email_notification(user, tournament):
    subject = f'Напоминание: турнир {tournament.name} скоро начнется!'
    html_message = render_to_string('accounts/emails/tournament_reminder.html', {
        'user': user,
        'tournament': tournament,
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        None,  # Используется DEFAULT_FROM_EMAIL из settings.py
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )