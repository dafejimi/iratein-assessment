from rest_framework import serializers
from apps.chat.models import ChatMessage
from apps.users.serializers import CustomUserSerializer

class ChatMessageSerializer(serializers.ModelSerializer):
	userName = serializers.SerializerMethodField()
	userImage = serializers.ImageField(source='user.image')

	class Meta:
		model = ChatMessage
		exclude = ['id', 'chat']

	def get_userName(self, Obj):
		return Obj.user.first_name + ' ' + Obj.user.last_name
