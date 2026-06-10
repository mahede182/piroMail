from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from emails.models import Email, Configuration

def get_notifications(request):
    if request.method == 'GET':
        important_emails = Email.objects.filter(is_important=True).order_by('-created_at')
        
        data = []
        for email in important_emails:
            data.append({
                'email_id': email.email_id,
                'sender': email.sender,
                'subject': email.subject,
                'priority': email.priority,
                'category': email.category,
                'reason': email.reason,
            })
            
        return JsonResponse(data, safe=False)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def config_view(request):
    if request.method == 'GET':
        try:
            config = Configuration.objects.get(key='SYSTEM_PROMPT')
            return JsonResponse({'prompt': config.value})
        except Configuration.DoesNotExist:
            return JsonResponse({'prompt': ''})
            
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
