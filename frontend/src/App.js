import React, { useState } from 'react';
import RecruiterDashboard from './components/RecruiterDashboard';
import StudentDashboard from './components/StudentDashboard';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('recruiter');

  return (
    <div className="App">
      <header className="app-header">
        <h1>🎯 AI Resume Screening & Skill Gap Analyzer</h1>
        <div className="tab-buttons">
          <button 
            className={activeTab === 'recruiter' ? 'active' : ''}
            onClick={() => setActiveTab('recruiter')}
          >
            Recruiter Dashboard
          </button>
          <button 
            className={activeTab === 'student' ? 'active' : ''}
            onClick={() => setActiveTab('student')}
          >
            Student Dashboard
          </button>
        </div>
      </header>

      <main className="main-content">
        {activeTab === 'recruiter' ? <RecruiterDashboard /> : <StudentDashboard />}
      </main>

      <footer className="app-footer">
        <p>© 2025 AI Resume Screening System</p>
      </footer>
    </div>
  );
}

export default App;
