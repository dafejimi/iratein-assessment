import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.chat.models import ChatRoom, ChatMessage
from apps.user.models import User, OnlineUser

class ChatConsumer(AsyncWebsocketConsumer):
	def getUser(self, userId):
		return User.objects.get(id=userId)

	def saveMessage(self, message, userId):
		userObj = User.objects.get(id=userId)
		chatMessageObj = ChatMessage.objects.create(
			user=userObj, message=message
			#, timestamp=
		)
		return {
			'action': 'message',
			'user': userId,
			'message': message,
			'userName': userObj.first_name + " " + userObj.last_name,
			'timestamp': str(chatMessageObj.timestamp)
		}

	async def connect(self):
		self.userId = self.scope['url_route']['kwargs']['userId']
		await self.channel_layer.group_add('onlineUser', self.channel_name)
		self.user = await database_sync_to_async(self.getUser)(self.userId)
		await database_sync_to_async(self.addOnlineUser)(self.user)
		await self.sendOnlineUserList()
		await self.accept()

	async def disconnect(self, close_code):
		await database_sync_to_async(self.deleteOnlineUser)(self.user)
		await self.sendOnlineUserList()

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		action = text_data_json['action']
		roomId = text_data_json['roomId']
		chatMessage = {}
		if action == 'message':
			message = text_data_json['message']
			userId = text_data_json['user']
			chatMessage = await database_sync_to_async(
				self.saveMessage
			)(message, userId, roomId)
		elif action == 'typing':
			chatMessage = text_data_json
		await self.channel_layer.group_send(
			roomId,
			{
				'type': 'chat_message',
				'message': chatMessage
			}
		)

	async def chat_message(self, event):
		message = event['message']
		await self.send(text_data=json.dumps(message))
