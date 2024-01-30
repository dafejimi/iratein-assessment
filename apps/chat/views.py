from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from apps.chat.serializers import ChatMessageSerializer
from apps.chat.models import ChatMessage

class MessagesView(ListAPIView):
	serializer_class = ChatMessageSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		roomId = self.kwargs['roomId']
		return ChatMessage.objects.\
			filter(chat__roomId=roomId).order_by('-timestamp')
