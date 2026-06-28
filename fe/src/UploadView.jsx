import React, { useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertCircle } from 'lucide-react';

export default function UploadView() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jdText, setJdText] = useState('');
  const [jdTitle, setJdTitle] = useState('');
  
  const [uploadStatus, setUploadStatus] = useState({ resume: null, jd: null }); // 'uploading', 'success', 'error'

  const handleResumeUpload = async (e) => {
    e.preventDefault();
    if (!resumeFile) return;
    
    setUploadStatus(prev => ({ ...prev, resume: 'uploading' }));
    
    const formData = new FormData();
    formData.append('file', resumeFile);
    
    try {
      const res = await fetch('http://localhost:8000/api/upload_resume/', {
        method: 'POST',
        body: formData,
      });
      if (res.ok) {
        setUploadStatus(prev => ({ ...prev, resume: 'success' }));
      } else {
        setUploadStatus(prev => ({ ...prev, resume: 'error' }));
      }
    } catch (err) {
      setUploadStatus(prev => ({ ...prev, resume: 'error' }));
    }
  };

  const handleJDUpload = async (e) => {
    e.preventDefault();
    if (!jdText || !jdTitle) return;
    
    setUploadStatus(prev => ({ ...prev, jd: 'uploading' }));
    
    const blob = new Blob([jdText], { type: 'text/plain' });
    const formData = new FormData();
    formData.append('file', blob, 'jd.txt');
    
    try {
      const res = await fetch(`http://localhost:8000/api/upload_jd/?title=${encodeURIComponent(jdTitle)}`, {
        method: 'POST',
        body: formData,
      });
      if (res.ok) {
        setUploadStatus(prev => ({ ...prev, jd: 'success' }));
      } else {
        setUploadStatus(prev => ({ ...prev, jd: 'error' }));
      }
    } catch (err) {
      setUploadStatus(prev => ({ ...prev, jd: 'error' }));
    }
  };

  return (
    <div className="animate-fade-in" style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ marginBottom: '40px', textAlign: 'center' }}>
        <h2 style={{ fontSize: '2.5rem', marginBottom: '12px' }} className="gradient-text">Data Ingestion</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>Upload candidate resumes and job descriptions for the AI engine to process.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
        
        {/* Resume Upload Module */}
        <div className="glass-panel" style={{ padding: '32px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
            <div style={{ background: 'rgba(59, 130, 246, 0.2)', padding: '12px', borderRadius: '12px', color: 'var(--primary)' }}>
              <FileText size={24} />
            </div>
            <h3 style={{ fontSize: '1.4rem' }}>Candidate Resume</h3>
          </div>
          
          <form onSubmit={handleResumeUpload}>
            <div 
              style={{ 
                border: '2px dashed var(--border-light)', 
                borderRadius: '16px', 
                padding: '40px 24px', 
                textAlign: 'center',
                marginBottom: '24px',
                background: 'rgba(255,255,255,0.02)',
                cursor: 'pointer',
                transition: 'all 0.2s',
              }}
              onClick={() => document.getElementById('resume-upload').click()}
            >
              <UploadCloud size={48} color="var(--primary)" style={{ marginBottom: '16px', opacity: 0.8 }} />
              <h4 style={{ marginBottom: '8px' }}>Drag & Drop PDF</h4>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '16px' }}>or click to browse files</p>
              
              <input 
                type="file" 
                id="resume-upload" 
                hidden 
                accept=".pdf"
                onChange={(e) => setResumeFile(e.target.files[0])}
              />
              
              {resumeFile && (
                <div style={{ background: 'rgba(59, 130, 246, 0.1)', padding: '8px 16px', borderRadius: '8px', display: 'inline-block', color: 'var(--text-main)', fontSize: '0.9rem' }}>
                  {resumeFile.name}
                </div>
              )}
            </div>

            <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center' }} disabled={!resumeFile || uploadStatus.resume === 'uploading'}>
              {uploadStatus.resume === 'uploading' ? 'Analyzing via AI...' : 'Parse & Extract Skills'}
            </button>
            
            {uploadStatus.resume === 'success' && <div style={{ color: 'var(--accent)', marginTop: '16px', display: 'flex', alignItems: 'center', gap: '8px', justifyContent: 'center' }}><CheckCircle2 size={18} /> Resume indexed successfully!</div>}
            {uploadStatus.resume === 'error' && <div style={{ color: 'var(--danger)', marginTop: '16px', display: 'flex', alignItems: 'center', gap: '8px', justifyContent: 'center' }}><AlertCircle size={18} /> Parsing failed. Ensure backend is running.</div>}
          </form>
        </div>

        {/* JD Upload Module */}
        <div className="glass-panel" style={{ padding: '32px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
            <div style={{ background: 'rgba(139, 92, 246, 0.2)', padding: '12px', borderRadius: '12px', color: 'var(--secondary)' }}>
              <Briefcase size={24} />
            </div>
            <h3 style={{ fontSize: '1.4rem' }}>Job Description</h3>
          </div>
          
          <form onSubmit={handleJDUpload}>
            <div style={{ marginBottom: '20px' }}>
              <label style={{ display: 'block', marginBottom: '8px', color: 'var(--text-muted)' }}>Job Title</label>
              <input 
                type="text" 
                className="input-themed" 
                placeholder="e.g. Senior Data Scientist" 
                value={jdTitle}
                onChange={e => setJdTitle(e.target.value)}
                required
              />
            </div>
            
            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', marginBottom: '8px', color: 'var(--text-muted)' }}>Job Requirements</label>
              <textarea 
                className="input-themed" 
                placeholder="Paste the job description text here..." 
                rows="6"
                style={{ resize: 'vertical' }}
                value={jdText}
                onChange={e => setJdText(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center', background: 'linear-gradient(135deg, var(--secondary), var(--primary))' }} disabled={!jdTitle || !jdText || uploadStatus.jd === 'uploading'}>
              {uploadStatus.jd === 'uploading' ? 'Extracting Requiremets...' : 'Save Job Description'}
            </button>

            {uploadStatus.jd === 'success' && <div style={{ color: 'var(--accent)', marginTop: '16px', display: 'flex', alignItems: 'center', gap: '8px', justifyContent: 'center' }}><CheckCircle2 size={18} /> JD processed successfully!</div>}
            {uploadStatus.jd === 'error' && <div style={{ color: 'var(--danger)', marginTop: '16px', display: 'flex', alignItems: 'center', gap: '8px', justifyContent: 'center' }}><AlertCircle size={18} /> Processing failed. Ensure backend is running.</div>}
          </form>
        </div>

      </div>
    </div>
  );
}
