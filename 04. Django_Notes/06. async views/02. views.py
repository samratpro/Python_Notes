from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async
from .models import Conversation, Message

@require_POST
@csrf_exempt
async def send_message(request):
    try:
        conversation_id = request.POST.get('conversation_id')
        sender = request.POST.get('sender')
        text = request.POST.get('text')
        
        conversation = await sync_to_async(Conversation.objects.get)(pk=conversation_id)
        message = await sync_to_async(Message.objects.create)(
            conversation=conversation,
            sender=sender,
            text=text
        )
        return JsonResponse({'message': 'Message sent successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
async def get_messages(request, conversation_id):
    try:
        messages = await sync_to_async(Message.objects.filter)(conversation_id=conversation_id)
        data = [{'sender': message.sender, 'text': message.text, 'created_at': message.created_at} for message in messages]
        return JsonResponse({'messages': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
