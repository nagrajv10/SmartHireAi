import React, { useState, useEffect } from 'react';
import { Search, MapPin, Briefcase, Star, ChevronRight, TrendingUp } from 'lucide-react';

export default function Dashboard({ onNavigate }) {
  const [candidates, setCandidates] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);

  // Mock initial fetch or real fetch
  useEffect(() => {
    fetchCandidates('');
  }, []);

  const fetchCandidates = async (query) => {
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/api/search/?query=${encodeURIComponent(query)}`);
      if (res.ok) {
        const data = await res.json();
        setCandidates(data.results || []);
      } else {
        // Fallback mock data if backend not running yet
        setCandidates(getMockData(query));
      }
    } catch (e) {
      setCandidates(getMockData(query));
    }
    setLoading(false);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchCandidates(searchQuery);
  };

  return (
    <div className="animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
        <div>
          <h2 style={{ fontSize: '2rem', marginBottom: '8px' }}>Candidate Match Explorer</h2>
          <p style={{ color: 'var(--text-muted)', margin: 0 }}>Review AI-ranked candidates against your job descriptions.</p>
        </div>
        <button className="btn-primary" onClick={onNavigate}>
          Upload New Resume <ChevronRight size={18} />
        </button>
      </div>

      {/* Search Bar */}
      <div className="glass-panel" style={{ padding: '24px', marginBottom: '32px' }}>
        <form onSubmit={handleSearch} style={{ display: 'flex', gap: '16px' }}>
          <div style={{ position: 'relative', flex: 1 }}>
            <Search size={20} style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
            <input 
              type="text" 
              className="input-themed" 
              placeholder="Search by role, skills, or experience..." 
              style={{ paddingLeft: '48px' }}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <button type="submit" className="btn-primary">Search / Rank</button>
        </form>
      </div>

      {/* Results Grid */}
      <h3 style={{ marginBottom: '20px', color: 'var(--text-main)' }}>Ranked Candidates</h3>
      
      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>Analyzing profiles...</div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '24px' }}>
          {candidates.map((candidate, idx) => (
            <CandidateCard key={idx} candidate={candidate} rank={idx + 1} />
          ))}
          {candidates.length === 0 && (
            <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '60px', background: 'var(--bg-card)', borderRadius: '16px', border: '1px dashed var(--border-light)' }}>
              <p style={{ color: 'var(--text-muted)' }}>No matching candidates found.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function CandidateCard({ candidate, rank }) {
  // Derive a mock score if real backend matching isn't active
  const score = candidate.match_score || Math.max(0.4, 0.98 - (rank * 0.05));
  const scorePercentage = Math.round(score * 100);
  
  return (
    <div className="glass-panel" style={{ padding: '24px', position: 'relative', display: 'flex', flexDirection: 'column' }}>
      <div style={{ position: 'absolute', top: '24px', right: '24px', background: 'rgba(59, 130, 246, 0.2)', color: '#60a5fa', padding: '4px 12px', borderRadius: '12px', fontWeight: 'bold', fontSize: '0.85rem' }}>
        #{rank} Match
      </div>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px' }}>
        <div style={{ width: '56px', height: '56px', borderRadius: '16px', background: 'rgba(255,255,255,0.05)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem', fontWeight: 'bold', border: '1px solid var(--border-light)' }}>
          {candidate.name ? candidate.name.charAt(0).toUpperCase() : 'C'}
        </div>
        <div>
          <h3 style={{ margin: '0 0 4px 0', fontSize: '1.2rem' }}>{candidate.name || 'Unknown Candidate'}</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            <Briefcase size={14} /> {candidate.experience_years} years exp
          </div>
        </div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.9rem' }}>
          <span>Overall Match Score</span>
          <span style={{ fontWeight: 'bold', color: scorePercentage > 80 ? 'var(--accent)' : 'var(--primary)' }}>{scorePercentage}%</span>
        </div>
        <div className="progress-bg">
          <div className="progress-fill" style={{ width: `${scorePercentage}%`, background: scorePercentage > 80 ? 'var(--accent)' : '' }}></div>
        </div>
      </div>

      <div style={{ marginBottom: '24px', flex: 1 }}>
        <h4 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Top Skills</h4>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {(candidate.skills || []).slice(0, 5).map((skill, i) => (
            <span key={i} className="tag">{skill}</span>
          ))}
          {candidate.skills && candidate.skills.length > 5 && (
            <span className="tag" style={{ background: 'transparent', borderStyle: 'dashed' }}>+{candidate.skills.length - 5}</span>
          )}
        </div>
      </div>

      <button className="btn-secondary" style={{ width: '100%', justifyContent: 'center' }}>
        View AI Analysis
      </button>
    </div>
  );
}

// Helper to provide nice mock data if API is down
function getMockData(query) {
  return [
    { name: "Rahul Sharma", experience_years: 4.5, skills: ["Python", "React", "AWS", "Machine Learning", "FastAPI"], education: "B.Tech Computer Science" },
    { name: "Aisha Patel", experience_years: 3.0, skills: ["JavaScript", "React", "Node.js", "MongoDB", "Tailwind"], education: "B.Sc IT" },
    { name: "Omar Al-Fayed", experience_years: 6.2, skills: ["Python", "Data Science", "Scikit-Learn", "TensorFlow", "SQL"], education: "M.S. Data Science" },
    { name: "Sarah Jenkins", experience_years: 2.5, skills: ["React", "TypeScript", "Figma", "CSS"], education: "B.A. Design" }
  ].filter(c => !query || c.skills.some(s => s.toLowerCase().includes(query.toLowerCase())) || c.name.toLowerCase().includes(query.toLowerCase()));
}
