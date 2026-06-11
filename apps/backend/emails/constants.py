# Default Values
DEFAULT_AI_MODEL = 'openrouter/free'
DEFAULT_POLL_INTERVAL = 10
DEFAULT_MODEL_COST_STRING = '$0.00 (Free Tier)'

# Form Choices
AI_CHOICES = [
    ('openrouter/free', 'OpenRouter Free Tier (0$)'),
    ('google/gemini-2.5-flash-api', 'Gemini 2.5 Flash'),
    ('google/gemini-2.5-pro-api', 'Gemini 2.5 Pro'),
    ('gemma-4-26b-a4b-it:free', 'Gemma Free'),
    ('openai/gpt-4o-mini', 'GPT-4o Mini'),
    ('openai/gpt-4o', 'GPT-4o'),
    ('anthropic/claude-3.5-sonnet', 'Claude 3.5 Sonnet'),
]

# AI Prompts
DEFAULT_BASE_PROMPT = (
    "You are an AI Email Assistant classifying an email. "
    "Analyze the following email subject and body.\n\n"
    "What the AI Should Flag as Important:\n"
    "• Client complaint or urgent customer request\n"
    "• Payment failure or billing issue\n"
    "• Low-priority automated or subscription email (Do NOT flag as important)\n"
)

JSON_INSTRUCTION_PROMPT = (
    "You must return ONLY a raw JSON object with NO markdown formatting, NO code blocks, and NO extra text. "
    "The JSON object must have exactly these keys: "
    "1. 'important' (boolean): true if the email is urgent, action-required, or from a critical sender (boss, client, alert). "
    "2. 'priority' (string): either 'HIGH', 'MEDIUM', or 'LOW'. "
    "3. 'category' (string): a short 1-2 word category (e.g., 'Work', 'Alert', 'Newsletter'). "
    "4. 'reason' (string): a clear sentence justifying the decision. "
)

ADMIN_HELP_TEXT_POLL_INTERVAL = "Background and frontend polling interval in seconds."
ADMIN_HELP_TEXT_AI_MODEL = "Select the AI model for classifying incoming emails."
ADMIN_HELP_TEXT_SYSTEM_PROMPT = "The strict instruction prompt sent to the AI model. Ensure it mandates a JSON response."
