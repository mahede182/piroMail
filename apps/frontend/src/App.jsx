import { useState, useEffect } from 'react';
import './index.css';

const API_URL = 'http://localhost:8000/api/notifications/';
const CONFIG_URL = 'http://localhost:8000/api/config/';
const POLL_INTERVAL_MS = 10000;

function App() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [systemPrompt, setSystemPrompt] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');
  const [lastUpdated, setLastUpdated] = useState(null);

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

  useEffect(() => {
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
      } catch (e) {
        console.error("Fetching error:", e);
        setError("Failed to fetch notifications.");
      } finally {
        setLoading(false);
      }
    };

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

  const getPriorityColor = (priority) => {
    switch (priority.toLowerCase()) {
      case 'high': return '#ff4d4f';
      case 'medium': return '#faad14';
      default: return '#52c41a';
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>PiroMail</h1>
        <div className="profile">
          <div className="avatar">AI</div>
          <div className="user-info">
            <span className="name">User</span>
            <span className="dropdown-arrow">▼</span>
          </div>
        </div>
      </header>

      <div className="main-container">
        <aside className="left-panel-narrow">
          <h2>Email Reading Agent System Prompt</h2>
          <textarea
            className="system-input"
            rows={8}
            value={systemPrompt}
            onChange={(e) => setSystemPrompt(e.target.value)}
            placeholder="Enter instructions for how the AI should read and respond to emails..."
          />
          <div className="button-row">
            <button onClick={handleSavePrompt} disabled={isSaving} className="primary-btn">
              {isSaving ? 'Saving...' : 'Save Prompt'}
            </button>
            {saveMessage && <span className="save-message">{saveMessage}</span>}
          </div>
          <h3 style={{ marginTop: '1.5rem', fontSize: '0.85rem', color: '#888', textTransform: 'uppercase' }}>Active Tools</h3>
          <ul className="tools-list">
            <li>labelemail</li>
            <li>extractpriority</li>
          </ul>
        </aside>

        <section className="right-panel">
          <div className="inbox-header">
            <div className="inbox-actions">
              <span className="inbox-title">Important Emails</span>
            </div>
            <div className="inbox-status">
              {lastUpdated && (
                <span className="last-updated">
                  Last updated: {lastUpdated.toLocaleTimeString()}
                </span>
              )}
            </div>
          </div>

          <div className="email-tabs">
            <button className="tab-button active">
              Inbox ({emails.length})
            </button>
          </div>

          <div className="email-list">
            {loading && <div className="loading">Loading your intelligence...</div>}
            {error && <div className="error">{error}</div>}

            {!loading && !error && emails.length === 0 && (
              <div className="empty-state">
                <p>No urgent notifications at the moment.</p>
              </div>
            )}

            {!loading && !error && emails.map((email) => (
              <div key={email.email_id} className="email-item-compact">
                <div className="email-content">
                  <span className="sender-name">{email.sender}</span>
                  <span className="email-separator">•</span>
                  <span className="email-subject">{email.subject}</span>
                  <span className="email-preview">{email.reason}</span>
                </div>
                <div className="email-status">
                  <span className="email-tag" style={{ backgroundColor: getPriorityColor(email.priority) }}>
                    {email.priority}
                  </span>
                  <span className="status-tag-compact processed">{email.category}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

export default App;
