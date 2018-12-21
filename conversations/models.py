from django.db import models
from core import models as core_models
from users.models import User

class Conversation(core_models.TimeStampedModel):
    participants = models.ManyToManyField(User, related_name="conversation", blank=True)
    def __str__(self): return " - ".join([user.username for user in self.participants.all()])
    def count_messages(self): return self.messages.count()
    def count_participants(self): return self.participants.count()

class Message(core_models.TimeStampedModel):
    message = models.TextField()
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    def __str__(self): return f"{self.user} says: {self.message}"