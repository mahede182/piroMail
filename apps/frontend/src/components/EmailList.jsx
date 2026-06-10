import React from 'react';

export default function EmailList({
  emails,
  loading,
  error,
  lastUpdated,
  onSelectEmail,
  isConnected
}) {
  const getPriorityColor = (priority) => {
    if (!priority) return 'var(--color-low)';
    switch (priority.toLowerCase()) {
      case 'high': return 'var(--color-high)';
      case 'medium': return 'var(--color-medium)';
      default: return 'var(--color-low)';
    }
  };

  const formatTime = (isoString) => {
    if (!isoString) return '';
    const date = new Date(isoString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <section className="email-list-container">
      <div className="inbox-header">
        <div className="email-tabs">
          <h2 className="dashboard-title">Important Notifications</h2>
        </div>
        <div className="inbox-status">
          {lastUpdated && (
            <span className="last-updated">
              Last updated: {lastUpdated.toLocaleTimeString()}
            </span>
          )}
        </div>
      </div>

      <div className="email-list">
        {loading && <div className="loading">Loading your intelligence...</div>}
        {error && <div className="error">{error}</div>}

        {!loading && !error && !isConnected && emails.length === 0 && (
          <div className="mock-mode-placeholder">
            <div className="mock-badge">Mock</div>
            <h3>Mock Mode Active</h3>
            <p>Connect your email to start real-time monitoring, or press "Poll Emails" in the header to run classification on mock data.</p>
          </div>
        )}

        {!loading && !error && isConnected && emails.length === 0 && (
          <div className="empty-state">
            <p>No important notifications found.</p>
          </div>
        )}

        {!loading && !error && (isConnected || emails.length > 0) && emails.map((email) => (
          <div 
            key={email.email_id} 
            className="email-item"
            onClick={() => onSelectEmail(email)}
          >
            <div className="email-header">
              <span className="sender-name">{email.sender}</span>
              <div className="email-status">
                {email.priority && (
                  <span className="priority-badge" style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.75rem', fontWeight: '600', color: getPriorityColor(email.priority) }}>
                    <span className="priority-dot" style={{ backgroundColor: getPriorityColor(email.priority) }}></span>
                    {email.priority}
                  </span>
                )}
                {email.category && <span className="category-tag">{email.category}</span>}
                <span className="email-time">{formatTime(email.created_at)}</span>
              </div>
            </div>
            <div className="email-subject">{email.subject}</div>
            <div className="email-preview">{email.reason || 'No reason provided'}</div>
          </div>
        ))}
      </div>
    </section>
  );
}

