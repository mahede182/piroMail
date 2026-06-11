from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.management import call_command
from emails.models import Email, Configuration

def get_notifications(request):
    if request.method == 'GET':
        emails = Email.objects.filter(is_important=True).order_by('-created_at')
        
        data = []
        for email in emails:
            data.append({
                'email_id': email.email_id,
                'sender': email.sender,
                'subject': email.subject,
                'body': email.body,
                'is_important': email.is_important,
                'priority': email.priority,
                'category': email.category,
                'reason': email.reason,
                'created_at': email.created_at.isoformat() if email.created_at else None,
            })
            
        return JsonResponse(data, safe=False)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def process_emails_view(request):
    if request.method == 'POST':
        try:
            call_command('poll_emails')
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_email(request, email_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = Email.objects.get(email_id=email_id)
            if 'body' in data:
                email.body = data['body']
                email.save()
            return JsonResponse({'status': 'success'})
        except Email.DoesNotExist:
            return JsonResponse({'error': 'Email not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def config_view(request):
    if request.method == 'GET':
        from emails.constants import DEFAULT_POLL_INTERVAL
        prompt = ''
        poll_interval = DEFAULT_POLL_INTERVAL * 1000
        try:
            prompt_config = Configuration.objects.get(key='SYSTEM_PROMPT')
            prompt = prompt_config.value
        except Configuration.DoesNotExist:
            pass
            
        try:
            poll_config = Configuration.objects.get(key='POLL_INTERVAL')
            poll_interval = int(poll_config.value) * 1000  # Convert to ms for frontend
        except (Configuration.DoesNotExist, ValueError):
            pass
            
        return JsonResponse({
            'prompt': prompt,
            'poll_interval': poll_interval
        })
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            Configuration.objects.update_or_create(
                key='SYSTEM_PROMPT',
                defaults={'value': prompt}
            )
            # Clear all classified emails so that they can be re-polled/re-processed with the new prompt
            Email.objects.all().delete()
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)
