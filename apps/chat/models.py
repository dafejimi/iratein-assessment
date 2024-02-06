from django.db import models
from shortuuidfield import ShortUUIDField
from apps.users.models import CustomUser

class ChatMessage(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
	message = models.CharField(max_length=255)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.message
