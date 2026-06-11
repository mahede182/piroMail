import React from 'react';

export default function Sidebar({
  systemPrompt,
  setSystemPrompt,
  handleSavePrompt,
  isSaving,
  saveMessage,
  handleProcessEmails,
  isProcessing
}) {
  return (
    <aside className="left-panel-narrow">
      <div className="prompt-section">
        <h2>Email Reading Agent System Prompt</h2>
        <textarea
          className="system-input"
          rows={8}
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
          placeholder="Enter instructions for how the AI should read and respond to emails..."
        />
        <div className="button-row-inline">
          <button onClick={handleSavePrompt} disabled={isSaving} className="btn-primary">
            {isSaving ? 'Saving...' : 'Save Prompt'}
          </button>
          <button 
            onClick={handleProcessEmails} 
            disabled={isProcessing} 
            className="btn-secondary"
          >
            {isProcessing ? 'Processing...' : 'Process Emails'}
          </button>
        </div>
        {saveMessage && <div className="save-message">{saveMessage}</div>}
        
        <div className="tools-section">
          <h3>Active Tools</h3>
          <ul className="tools-list">
            <li>labelemail</li>
            <li>extractpriority</li>
          </ul>
        </div>
      </div>
    </aside>
  );
}

