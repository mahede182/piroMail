import React, { useState, useEffect } from 'react';

export default function EmailDetail({ email, onBack, onSave }) {
  const [body, setBody] = useState(email.body || '');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    setBody(email.body || '');
  }, [email]);

  const handleSave = async () => {
    setIsSaving(true);
    await onSave(email.email_id, body);
    setIsSaving(false);
  };

  return (
    <section className="email-detail-container">
      <div className="detail-header">
        <button className="btn-back" onClick={onBack}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '2px' }}>
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Back
        </button>
        <button 
          className="btn-primary btn-save" 
          onClick={handleSave} 
          disabled={isSaving || body === email.body}
        >
          {isSaving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>
      
      <div className="detail-main-content">
        <h2 className="detail-subject">{email.subject}</h2>
        <div className="meta-row">
          <span className="meta-label">From:</span>
          <span className="meta-value">{email.sender}</span>
        </div>
        
        <div className="detail-body-editor">
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            className="body-textarea"
            placeholder="Email body content..."
          />
        </div>
      </div>
      
      <div className="detail-classification-footer">
        <div className="meta-row tags-row">
          {email.priority && <span className="meta-tag priority">{email.priority}</span>}
          {email.category && <span className="meta-tag category">{email.category}</span>}
        </div>
        {email.reason && (
          <div className="reason-section">
            <span className="meta-label">AI Reason:</span>
            <p className="reason-text">{email.reason}</p>
          </div>
        )}
      </div>
    </section>
  );
}
