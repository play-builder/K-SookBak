from django.db import models
from core import models as core_models
from users.models import User
from rooms.models import Room

class Review(core_models.TimeStampedModel):
    review = models.TextField()
    accuracy = models.IntegerField()
    communications = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name="reviews", on_delete=models.CASCADE)

    def __str__(self): return f"{self.review} - {self.room}"
    def rating_average(self):
        avg = (self.accuracy + self.communications + self.cleanliness + self.location + self.check_in + self.value) / 6
        return round(avg, 2)