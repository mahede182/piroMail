from django import template
from django.utils import timezone
from datetime import timedelta
import json
from emails.models import Email, Configuration
from emails.constants import (
    DEFAULT_AI_MODEL,
    DEFAULT_POLL_INTERVAL,
    DEFAULT_MODEL_COST_STRING
)

register = template.Library()

@register.inclusion_tag('admin/dashboard_stats.html')
def render_dashboard_stats():
    email_count = Email.objects.count()
    
    today = timezone.now().date()
    start_date = today - timedelta(days=6)
    
    # Simple aggregation in Python to ensure compatibility across SQLite/Postgres timezone handling
    emails_last_7_days = Email.objects.filter(created_at__date__gte=start_date)
    
    counts_by_date = {}
    for e in emails_last_7_days:
        d = e.created_at.date()
        counts_by_date[d] = counts_by_date.get(d, 0) + 1
        
    chart_labels = []
    chart_data = []
    
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        chart_labels.append(current_date.strftime('%b %d'))
        chart_data.append(counts_by_date.get(current_date, 0))
    
    ai_model_config = Configuration.objects.filter(key='AI_MODEL').first()
    ai_model = ai_model_config.value if ai_model_config else DEFAULT_AI_MODEL
    
    poll_interval_config = Configuration.objects.filter(key='POLL_INTERVAL').first()
    poll_interval = poll_interval_config.value if poll_interval_config else str(DEFAULT_POLL_INTERVAL)

    model_cost = DEFAULT_MODEL_COST_STRING

    return {
        'email_count': email_count,
        'ai_model': ai_model,
        'model_cost': model_cost,
        'poll_interval': poll_interval,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
