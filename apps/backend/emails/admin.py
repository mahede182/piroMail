from django.contrib import admin
from django.contrib.auth.models import Group, User
from django import forms
from emails.models import Configuration
from emails.constants import (
    AI_CHOICES,
    ADMIN_HELP_TEXT_POLL_INTERVAL,
    ADMIN_HELP_TEXT_AI_MODEL,
    ADMIN_HELP_TEXT_SYSTEM_PROMPT
)

admin.site.unregister(Group)
admin.site.unregister(User)

class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            key = self.instance.key
            if key == 'POLL_INTERVAL':
                self.fields['value'].widget = forms.NumberInput(attrs={
                    'min': '1', 
                    'step': '1',
                    'style': 'width: 150px; padding: 5px;'
                })
                self.fields['value'].help_text = ADMIN_HELP_TEXT_POLL_INTERVAL
            
            elif key == 'AI_MODEL':
                self.fields['value'].widget = forms.Select(
                    choices=AI_CHOICES,
                    attrs={'style': 'padding: 5px; width: 300px;'}
                )
                self.fields['value'].help_text = ADMIN_HELP_TEXT_AI_MODEL
            
            elif key == 'SYSTEM_PROMPT':
                self.fields['value'].widget = forms.Textarea(attrs={
                    'rows': 15, 
                    'style': 'font-family: monospace; width: 100%; padding: 10px; border-radius: 4px;'
                })
                self.fields['value'].help_text = ADMIN_HELP_TEXT_SYSTEM_PROMPT

@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    form = ConfigurationForm
    list_display = ('key', 'value_display', 'updated_at')
    search_fields = ('key', 'value')
    readonly_fields = ('key', 'updated_at')
    
    def value_display(self, obj):
        if len(obj.value) > 60:
            return f"{obj.value[:60]}..."
        return obj.value
    value_display.short_description = 'Value'

    def has_add_permission(self, request):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
