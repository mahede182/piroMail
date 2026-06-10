import json
import os
import time
from pathlib import Path

import google.generativeai as genai
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from emails.models import Email

class Command(BaseCommand):
    help = 'Polls mock_emails.json and processes new emails with Gemini.'

    def handle(self, *args, **options):
        gemini_api_key = os.environ.get('GEMINI_API_KEY')
        if not gemini_api_key:
            self.stderr.write(self.style.ERROR("GEMINI_API_KEY environment variable is not set."))
            return

        genai.configure(api_key=gemini_api_key)
        
        model = genai.GenerativeModel('gemini-2.5-flash')

        mock_file_path = settings.BASE_DIR / 'mock_emails.json'
        
        if not mock_file_path.exists():
            self.stderr.write(self.style.ERROR(f"Mock file not found at {mock_file_path}"))
            return

        try:
            with open(mock_file_path, 'r', encoding='utf-8') as f:
                emails_data = json.load(f)
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("Invalid JSON in mock_emails.json"))
            return

        for email_data in emails_data:
            email_id = email_data.get('email_id')
            sender = email_data.get('sender', 'Unknown')
            subject = email_data.get('subject', 'No Subject')
            body = email_data.get('body', '')

            if not email_id:
                self.stderr.write(self.style.WARNING("Skipping email without email_id."))
                continue

            if Email.objects.filter(email_id=email_id).exists():
                self.stdout.write(f"Skipping duplicate email_id: {email_id}")
                continue

            self.stdout.write(f"Processing new email: {email_id} - {subject}")

            from emails.models import Configuration
            try:
                config = Configuration.objects.get(key='SYSTEM_PROMPT')
                base_prompt = config.value
            except Configuration.DoesNotExist:
                base_prompt = (
                    "You are an AI Email Assistant classifying an email. "
                    "Analyze the following email subject and body."
                )

            system_prompt = (
                f"{base_prompt} "
                "You must return ONLY a raw JSON object with NO markdown formatting, NO code blocks, and NO extra text. "
                "The JSON object must have exactly these keys: "
                "1. 'important' (boolean): true if the email is urgent, action-required, or from a critical sender (boss, client, alert). "
                "2. 'priority' (string): either 'HIGH', 'MEDIUM', or 'LOW'. "
                "3. 'category' (string): a short 1-2 word category (e.g., 'Work', 'Alert', 'Newsletter'). "
                "4. 'reason' (string): a short explanation of why it was classified this way. "
                f"\n\nSubject: {subject}\nBody: {body}"
            )

            try:
                response = model.generate_content(system_prompt)
                response_text = response.text.strip()
                
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
                self.stdout.write(self.style.SUCCESS(f"Successfully processed and saved {email_id}."))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing email {email_id}: {str(e)}"))
                continue

            # Sleep slightly to avoid hitting API rate limits
            time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Finished polling mock emails."))
