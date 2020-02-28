from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from . models import Comment
from django.utils import timezone


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        fires when connect
        """
        self.task_id = self.scope['url_route']['kwargs']['pk']
        self.comment_group = 'comments_%s' % self.task_id

        # Join comments group
        await self.channel_layer.group_add(
            self.comment_group,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        """leave comments group"""
        await self.channel_layer.group_discard(
            self.comment_group,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Fires when data is received from js
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        task_id = text_data_json['related_task_id']
        time = timezone.now()
        await self.create_comment(sender, message, task_id, time)

        # Post comment to comment group
        await self.channel_layer.group_send(
            self.comment_group,
            {
                'type': 'post_comment',
                'message': message
            }
        )

    async def post_comment(self, event):
        """
        callback function to a group
        """
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def create_comment(self, sender, message, task_id, time):
        """
        Async function to create a Comment
        """
        comment = Comment(comment_sender=sender,
                          comment_text=message,
                          comment_related_task_id=task_id,
                          comment_date=time)

        comment.save()
