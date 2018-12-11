from django.db import models
from django.utils import timezone
from core import models as core_models
from users.models import User
from rooms.models import Room

class Reservation(core_models.TimeStampedModel):
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"
    STATUS_CHOICES = ((STATUS_PENDING, "Pending"), (STATUS_CONFIRMED, "Confirmed"), (STATUS_CANCELED, "Canceled"))

    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    guest = models.ForeignKey(User, related_name="reservations", on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name="reservations", on_delete=models.CASCADE)

    def __str__(self): return f"{self.room} - {self.check_in}"
    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out
    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out