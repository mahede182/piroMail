import React from 'react';

export default function EmailDetail({ email, onBack }) {
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
      </div>
      
      <div className="detail-main-content" style={{ overflowY: 'auto' }}>
        <h2 className="detail-subject">{email.subject}</h2>
        <div className="meta-row">
          <span className="meta-label">From:</span>
          <span className="meta-value">{email.sender}</span>
        </div>
        
        <div className="detail-body-editor" style={{ marginTop: '1.5rem' }}>
          <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6', fontSize: '1rem', color: 'var(--text-primary)' }}>
            {email.body}
          </div>
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

