import { useState, useEffect } from 'react';
import './index.css';
import Sidebar from './components/Sidebar';
import EmailList from './components/EmailList';
import EmailDetail from './components/EmailDetail';

const API_URL = 'http://localhost:8000/api/notifications/';
const CONFIG_URL = 'http://localhost:8000/api/config/';
const PROCESS_URL = 'http://localhost:8000/api/process_emails/';
const UPDATE_URL = 'http://localhost:8000/api/update_email/';
const POLL_INTERVAL_MS = 10000;

function App() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const isConnected = false;

  const [systemPrompt, setSystemPrompt] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');

  const [lastUpdated, setLastUpdated] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const [selectedEmail, setSelectedEmail] = useState(null);

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const response = await fetch(CONFIG_URL);
        if (response.ok) {
          const data = await response.json();
          setSystemPrompt(data.prompt || '');
        }
      } catch (e) {
        console.error("Failed to fetch config", e);
      }
    };
    fetchConfig();
  }, []);

  const fetchEmails = async () => {
    try {
      const response = await fetch(API_URL);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setEmails(data);
      setError(null);
      setLastUpdated(new Date());

      // Update selected email if it's currently open
      if (selectedEmail) {
        const updatedSelected = data.find(e => e.email_id === selectedEmail.email_id);
        if (updatedSelected) {
          setSelectedEmail(updatedSelected);
        }
      }
    } catch (e) {
      console.error("Fetching error:", e);
      setError("Failed to fetch notifications.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmails();
    const intervalId = setInterval(fetchEmails, POLL_INTERVAL_MS);
    return () => clearInterval(intervalId);
  }, []);

  const handleSavePrompt = async () => {
    setIsSaving(true);
    setSaveMessage('');
    try {
      const response = await fetch(CONFIG_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: systemPrompt }),
      });
      if (response.ok) {
        setSaveMessage('Saved!');
        setTimeout(() => setSaveMessage(''), 3000);
      } else {
        setSaveMessage('Error saving.');
      }
    } catch (e) {
      console.error("Failed to save config", e);
      setSaveMessage('Error saving.');
    } finally {
      setIsSaving(false);
    }
  };

  const handleProcessEmails = async () => {
    setIsProcessing(true);
    try {
      const response = await fetch(PROCESS_URL, { method: 'POST' });
      if (response.ok) {
        await fetchEmails();
      } else {
        console.error("Failed to process emails");
      }
    } catch (e) {
      console.error("Process error:", e);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleUpdateEmail = async (emailId, newBody) => {
    try {
      const response = await fetch(`${UPDATE_URL}${emailId}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ body: newBody })
      });
      if (response.ok) {
        await fetchEmails();
      }
    } catch (e) {
      console.error("Failed to update email:", e);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>PiroMail</h1>
        <div className="header-controls">
          <button 
            onClick={handleProcessEmails} 
            disabled={isProcessing} 
            className="btn-primary header-btn"
          >
            {isProcessing ? 'Polling...' : 'Poll Mock Emails'}
          </button>
        </div>
      </header>

      <div className="main-container">
        <Sidebar
          systemPrompt={systemPrompt}
          setSystemPrompt={setSystemPrompt}
          handleSavePrompt={handleSavePrompt}
          isSaving={isSaving}
          saveMessage={saveMessage}
          handleProcessEmails={handleProcessEmails}
          isProcessing={isProcessing}
        />

        <div className="right-panel">
          {selectedEmail ? (
            <EmailDetail
              email={selectedEmail}
              onBack={() => setSelectedEmail(null)}
              onSave={handleUpdateEmail}
            />
          ) : (
            <EmailList
              emails={emails}
              loading={loading}
              error={error}
              lastUpdated={lastUpdated}
              onSelectEmail={setSelectedEmail}
              isConnected={isConnected}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

