# AI Email Assistant - Agent Instructions

## Global Context
[cite_start]**Project Type:** Personal Project 
**Goal:** Build a locally hosted, AI-powered email assistant that reads a mock inbox, classifies emails using Google Gemini, and displays important notifications on a dashboard.
[cite_start]**Architecture Motif:** Inspired by `DispatchMail`  (local SQLite storage, agent-based monitoring https://github.com/dbish/DispatchMail).
**Tech Stack:** Python/Django (Backend), Vite/React (Frontend), Docker (DevOps).
**Core Principle:** KISS (Keep It Simple, Stupid). [cite_start]Do not over-engineer[cite: 84]. Follow best practice.

---

## Agent Tasks & Execution Flow

### Task 1: The Django Data Layer (Duplicate Prevention)
**Role:** Django Backend Engineer
[cite_start]**Instruction:** Write the `models.py` file for the Django backend to handle duplicate prevention and store AI classification results[cite: 82].
**Requirements:**
* Create an `Email` model.
* [cite_start]Include the following fields exactly: `email_id` (string, unique), `sender` (string), `subject` (string), `body` (text), `is_important` (boolean), `priority` (choices: HIGH, MEDIUM, LOW), `category` (string), and `reason` (text)[cite: 83].

### Task 2: The AI Core & Polling Engine
**Role:** Django Backend Engineer
[cite_start]**Instruction:** Write the core processing engine as a Django Management Command (`management/commands/poll_emails.py`)[cite: 85].
**Requirements:**
* [cite_start]Read incoming emails from a local `mock_emails.json` file[cite: 85].
* [cite_start]Check the SQLite database to ensure the email hasn't been processed yet[cite: 85].
* [cite_start]If it is a new email, send the subject and body to the Google Gemini API (using `google-generativeai`)[cite: 85].
* [cite_start]**Crucial AI Prompting:** Write a strict system prompt for Gemini to guarantee it returns a JSON object with exactly these keys: `important` (boolean), `priority` (string), `category` (string), and `reason` (string)[cite: 86].
* [cite_start]Save the parsed result to the Django database[cite: 86].

### Task 3: Exposing the Data via API
**Role:** Django Backend Engineer
[cite_start]**Instruction:** Expose the processed data to the React frontend by writing the `views.py` and `urls.py`[cite: 88].
**Requirements:**
* [cite_start]Use Django REST Framework (DRF) or simple `JsonResponse`[cite: 88].
* [cite_start]Create a `GET /api/notifications/` endpoint[cite: 88].
* [cite_start]Query the SQLite database and return only the emails where `is_important` is True, ordered by the newest first[cite: 88]. Keep the view minimal.

### Task 4: The React Dashboard UI
**Role:** Frontend React Developer
**Instruction:** Build the frontend interface to consume the Django API. [cite_start]Write a complete `App.jsx` component[cite: 90].
**Requirements:**
* [cite_start]Fetch data from `http://localhost:8000/api/notifications/`[cite: 90].
* [cite_start]Implement a `setInterval` polling mechanism in a `useEffect` to re-fetch this data every 10 seconds[cite: 90].
* [cite_start]Render the important emails as a grid of notification cards[cite: 90].
* [cite_start]Each card must display the Sender, Subject, Priority, Category, and Reason[cite: 90].
* [cite_start]Use simple inline styles or basic Tailwind classes to add a visual indicator (like a colored border: Red for HIGH, Yellow for MEDIUM, Gray for LOW) based on the priority[cite: 90, 91].

### Task 5: Containerization (Docker)
**Role:** DevOps Engineer
[cite_start]**Instruction:** Containerize the full-stack application so it runs locally on a macOS environment with a simple `docker compose up --build`[cite: 92].
**Requirements:**
* [cite_start]**Backend Dockerfile:** Use `python:3.11-slim`, install requirements, run migrations, and start the Django server[cite: 92].
* [cite_start]**Frontend Dockerfile:** Create a multi-stage build (build with Node, serve static files with Nginx)[cite: 92].
* [cite_start]**docker-compose.yml:** Define both services at the root, link them, map the ports (Django on 8000, React on 3000), and handle environment variables[cite: 92, 93]. Keep the configuration as simple as possible.