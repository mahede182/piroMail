import json
import os
import time
from pathlib import Path

from openai import OpenAI
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from emails.models import Email

class Command(BaseCommand):
    help = 'Polls mock_emails.json and processes new emails with Gemini.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--loop',
            action='store_true',
            help='Continuously poll the inbox on a set interval (e.g. every 2 minutes)',
        )

    def handle(self, *args, **options):
        openrouter_api_key = os.environ.get('OPENROUTER_API_KEY')
        if not openrouter_api_key:
            self.stderr.write(self.style.ERROR("OPENROUTER_API_KEY environment variable is not set."))
            return

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_api_key,
        )

        mock_file_path = settings.BASE_DIR / 'mock_emails.json'
        
        if not mock_file_path.exists():
            self.stderr.write(self.style.ERROR(f"Mock file not found at {mock_file_path}"))
            return

        is_loop = options['loop']
        
        while True:
            try:
                with open(mock_file_path, 'r', encoding='utf-8') as f:
                    emails_data = json.load(f)
            except json.JSONDecodeError:
                self.stderr.write(self.style.ERROR("Invalid JSON in mock_emails.json"))
                if is_loop:
                    time.sleep(120)
                    continue
                return

            new_emails_processed = 0

            for email_data in emails_data:
                email_id = email_data.get('email_id')
                sender = email_data.get('sender', 'Unknown')
                subject = email_data.get('subject', 'No Subject')
                body = email_data.get('body', '')

                if not email_id:
                    self.stderr.write(self.style.WARNING("Skipping email without email_id."))
                    continue

                if Email.objects.filter(email_id=email_id).exists():
                    # Silently skip duplicates to avoid spamming stdout during loop
                    continue

                self.stdout.write(f"Processing new email: {email_id} - {subject}")

                from emails.models import Configuration
                from emails.constants import (
                    DEFAULT_BASE_PROMPT,
                    JSON_INSTRUCTION_PROMPT,
                    DEFAULT_AI_MODEL,
                )

                try:
                    config = Configuration.objects.get(key='SYSTEM_PROMPT')
                    base_prompt = config.value
                except Configuration.DoesNotExist:
                    base_prompt = DEFAULT_BASE_PROMPT

                system_prompt = (
                    f"{base_prompt} "
                    f"{JSON_INSTRUCTION_PROMPT} "
                    f"\n\nSubject: {subject}\nBody: {body}"
                )

                try:
                    ai_model_config = Configuration.objects.get(key='AI_MODEL')
                    ai_model = ai_model_config.value
                except Configuration.DoesNotExist:
                    ai_model = DEFAULT_AI_MODEL

                try:
                    response = client.chat.completions.create(
                        model=ai_model,
                        messages=[
                            {
                                "role": "system",
                                "content": system_prompt
                            }
                        ]
                    )
                    response_text = response.choices[0].message.content.strip()
                    
                    # Sanitize response to ensure it's valid JSON
                    if response_text.startswith("```json"):
                        response_text = response_text[7:]
                    if response_text.startswith("```"):
                        response_text = response_text[3:]
                    if response_text.endswith("```"):
                        response_text = response_text[:-3]
                    response_text = response_text.strip()

                    ai_result = json.loads(response_text)
                    
                    is_important = ai_result.get('important', False)
                    priority = ai_result.get('priority', 'LOW').upper()
                    if priority not in ['HIGH', 'MEDIUM', 'LOW']:
                        priority = 'LOW'
                    category = ai_result.get('category', 'General')
                    reason = ai_result.get('reason', 'No reason provided')

                    with transaction.atomic():
                        Email.objects.create(
                            email_id=email_id,
                            sender=sender,
                            subject=subject,
                            body=body,
                            is_important=is_important,
                            priority=priority,
                            category=category,
                            reason=reason
                        )
                    self.stdout.write(self.style.SUCCESS(f"Successfully processed and saved {email_id} using {ai_model}."))
                    new_emails_processed += 1

                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error processing email {email_id}: {str(e)}"))
                    continue

                # Sleep slightly to avoid hitting API rate limits
                time.sleep(1)

            if new_emails_processed == 0 and not is_loop:
                self.stdout.write(self.style.SUCCESS("No new mock emails to process."))
            elif new_emails_processed > 0:
                self.stdout.write(self.style.SUCCESS(f"Finished polling mock emails. Processed {new_emails_processed} new emails."))

            if not is_loop:
                break
                
            try:
                from emails.models import Configuration
                from emails.constants import DEFAULT_POLL_INTERVAL
                poll_interval_config = Configuration.objects.get(key='POLL_INTERVAL')
                poll_interval = int(poll_interval_config.value)
            except (Configuration.DoesNotExist, ValueError):
                poll_interval = DEFAULT_POLL_INTERVAL

            time.sleep(poll_interval)
