import React, { useState } from 'react';
import { Upload, Briefcase, BarChart } from 'lucide-react';
import UploadView from './UploadView';
import Dashboard from './Dashboard';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div>
          <h1 className="gradient-text" style={{ fontSize: '1.8rem', margin: '0 0 8px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Briefcase size={28} color="currentColor" /> SmartHire AI
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', margin: 0 }}>Next-Gen ATS Platform</p>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '20px' }}>
          <div 
            className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            <BarChart size={20} />
            <span>Dashboard</span>
          </div>
          <div 
            className={`nav-item ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            <Upload size={20} />
            <span>Upload Data</span>
          </div>
        </nav>
        
        <div style={{ marginTop: 'auto', padding: '16px', background: 'var(--bg-card)', borderRadius: '12px', border: '1px solid var(--border-light)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'linear-gradient(135deg, var(--primary), var(--secondary))', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>JD</div>
            <div>
              <div style={{ fontWeight: '500', fontSize: '0.9rem' }}>Jane Doe</div>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>HR Manager</div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {activeTab === 'dashboard' && <Dashboard onNavigate={() => setActiveTab('upload')} />}
        {activeTab === 'upload' && <UploadView />}
      </main>
    </div>
  );
}

export default App;
