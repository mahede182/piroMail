// The VITE_API_BASE_URL is loaded from the .env file. Fallback to localhost if missing.
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const API_URL = `${API_BASE_URL}/api/notifications/`;
export const CONFIG_URL = `${API_BASE_URL}/api/config/`;
export const PROCESS_URL = `${API_BASE_URL}/api/process_emails/`;
export const UPDATE_URL = `${API_BASE_URL}/api/update_email/`;
