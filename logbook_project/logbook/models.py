from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class LogbookEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logbook_entries', null=True)
    date = models.DateField(default=timezone.now)
    goals = models.TextField(verbose_name="Doelen van de dag/week")
    time_registration = models.TextField(verbose_name="Tijdregistratie")
    tasks_completed = models.TextField(verbose_name="Uitgevoerde taken")
    problems_challenges = models.TextField(verbose_name="Problemen en uitdagingen")
    solutions_learnings = models.TextField(verbose_name="Oplossingen en leerpunten")
    feedback_reflection = models.TextField(verbose_name="Feedback of reflectie")
    todo_next = models.TextField(verbose_name="To-do voor de volgende dag/week")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Logbook Entry for {self.user.username} on {self.date}"

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Logbook Entries"

class Goal(models.Model):
    TERM_CHOICES = [
        ('short', 'Short Term'),
        ('mid', 'Mid Term'),
        ('long', 'Long Term'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    term = models.CharField(max_length=5, choices=TERM_CHOICES)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_term_display()} Goal for {self.user.username}: {self.description[:50]}"

    class Meta:
        ordering = ['term', '-created_at']
