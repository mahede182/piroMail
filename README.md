# piroMail

AI-powered email assistant that reads inbox, classifies emails using AI, and displays important notifications on a real-time dashboard.

# preview


https://github.com/user-attachments/assets/858224a9-8c67-45a8-b489-556fca5faa92



## 🚀 Tech Stack

- **Backend:** Django 4.2+ (Python 3.11)
- **Database:** SQLite
- **AI Classification:** OpenRouter API
- **Frontend:** React, Vite
- **DevOps & Deployment:** Docker, Docker Compose, Render
- **Package Managers:** `uv` (Python), `npm` (Node.js)

## 🛠️ Configuration & Running the Application

### 1. Environment Setup

Create an `.env` file in the `apps/backend/` directory and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 2. Start the Services

Use Docker Compose to build and start both the frontend and backend services:

```bash
docker compose up --build
```
- **Backend API:** `http://localhost:8000`
- **Frontend Dashboard:** `http://localhost:3000`

### 3. Admin Credentials

| Username | Password |
|----------|----------|
| admin    | admin    |

### 4. Fetching and Classifying Emails (`poll_emails`)

To process the mock inbox and classify emails using the AI model, you need to run the `poll_emails` Django management command. 

If you are running the application via Docker Compose, you can trigger the email polling process by running:

```bash
docker compose exec backend python manage.py poll_emails
```

*This command will read the incoming mock emails, send them to the AI for classification, and store the important ones in the database. The frontend dashboard will then automatically poll and display these important notifications.*

## ⚠️ Limitations

- **Security:** Currently, we are using a mock inbox for testing purposes. In production, we would need to implement a more secure way to access and process emails.
- **Speed & Performance:** Currently, we are using a **free AI model** for the email classification via OpenRouter. Because of the rate limits and processing times of free tier models, the email classification process is a little bit slower.
