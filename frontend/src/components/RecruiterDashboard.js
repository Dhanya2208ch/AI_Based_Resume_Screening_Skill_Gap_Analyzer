import React, { useState } from 'react';
import axios from 'axios';
import './RecruiterDashboard.css';

const RecruiterDashboard = () => {
  const [resumes, setResumes] = useState([]);
  const [jobDescription, setJobDescription] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedCandidate, setSelectedCandidate] = useState(null);

  const handleFileChange = (e) => {
    setResumes(Array.from(e.target.files));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (resumes.length === 0 || !jobDescription) {
      alert('Please upload resumes and provide job description');
      return;
    }

    setLoading(true);

    const formData = new FormData();
    resumes.forEach(file => {
      formData.append('resumes', file);
    });
    formData.append('job_description', jobDescription);

    try {
      const response = await axios.post(
        'http://localhost:5000/api/upload-resumes',
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );

      setResults(response.data);
      alert('Screening completed successfully!');
    } catch (error) {
      console.error('Error:', error);
      alert('Error processing resumes: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const getScoreClass = (score) => {
    if (score >= 70) return 'high';
    if (score >= 50) return 'medium';
    return 'low';
  };

  return (
    <div className="recruiter-dashboard">
      <h2>📊 Recruiter Dashboard</h2>
      
      <div className="upload-section">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Upload Resumes (PDF/DOCX):</label>
            <input 
              type="file" 
              multiple 
              accept=".pdf,.docx"
              onChange={handleFileChange}
            />
            <p className="file-count">{resumes.length} file(s) selected</p>
          </div>

          <div className="form-group">
            <label>Job Description:</label>
            <textarea
              rows="8"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste job description here..."
            />
          </div>

          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Processing...' : 'Screen Resumes'}
          </button>
        </form>
      </div>

      {results && (
        <div className="results-section">
          <h3>Results ({results.total_candidates} candidates)</h3>

          <table className="results-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Name</th>
                <th>Email</th>
                <th>Match Score</th>
                <th>ATS Score</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {results.candidates.map((candidate, index) => (
                <tr key={index}>
                  <td>{index + 1}</td>
                  <td>{candidate.candidate_name}</td>
                  <td>{candidate.email}</td>
                  <td>
                    <span className={`score ${getScoreClass(candidate.match_score)}`}>
                      {candidate.match_score}%
                    </span>
                  </td>
                  <td>{candidate.ats_score}/100</td>
                  <td>
                    <button onClick={() => setSelectedCandidate(candidate)} className="view-btn">
                      View Full Analysis
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedCandidate && (
        <CandidateDetailModal 
          candidate={selectedCandidate}
          onClose={() => setSelectedCandidate(null)}
        />
      )}
    </div>
  );
};

const CandidateDetailModal = ({ candidate, onClose }) => {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>×</button>
        
        <h2>📋 {candidate.candidate_name}</h2>
        
        {/* Contact Information */}
        <div className="detail-section">
          <h3>📧 Contact Information</h3>
          <p><strong>Email:</strong> {candidate.email}</p>
          <p><strong>Phone:</strong> {candidate.phone}</p>
        </div>

        {/* Match Score & Explanation */}
        <div className="detail-section highlight-section">
          <h3>🎯 Match Score: {candidate.match_score}%</h3>
          <div className="explanation-box">
            <h4>AI Insights - Why This Score?</h4>
            <p className="assessment"><strong>Assessment:</strong> {candidate.explanation.overall_assessment}</p>
            <p className="recommendation"><strong>Recommendation:</strong> {candidate.explanation.recommendation}</p>
            <p className="explanation-text">{candidate.explanation.explanation}</p>
            
            {candidate.explanation.top_contributing_terms && candidate.explanation.top_contributing_terms.length > 0 && (
              <div className="contributing-terms">
                <h5>🔑 Key Matching Keywords:</h5>
                <div className="terms-list">
                  {candidate.explanation.top_contributing_terms.map((term, i) => (
                    <span key={i} className="term-badge">
                      {term.term} <small>({(term.importance * 100).toFixed(1)}%)</small>
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* ATS Score Breakdown */}
        <div className="detail-section">
          <h3>📊 ATS Score: {candidate.ats_score}/100</h3>
          <div className="ats-breakdown">
            {Object.entries(candidate.ats_breakdown).map(([key, value]) => (
              <div key={key} className="score-bar-container">
                <div className="score-label">
                  {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </div>
                <div className="score-bar">
                  <div 
                    className="score-fill" 
                    style={{
                      width: `${(value / getMaxScore(key)) * 100}%`,
                      backgroundColor: getScoreColor(value, getMaxScore(key))
                    }}
                  ></div>
                </div>
                <div className="score-value">{value}/{getMaxScore(key)}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Skills */}
        <div className="detail-section">
          <h3>💡 Skills ({candidate.skills.length})</h3>
          <div className="skills-list">
            {candidate.skills.map((skill, i) => (
              <span key={i} className="skill-tag">{skill}</span>
            ))}
          </div>
        </div>

        {/* Skill Gaps */}
        <div className="detail-section">
          <h3>🎯 Skill Gap Analysis</h3>
          {candidate.skill_gaps.missing_skills && candidate.skill_gaps.missing_skills.length > 0 ? (
            <div>
              <p className="gap-percentage">
                <strong>Gap:</strong> {candidate.skill_gaps.gap_percentage}% of required skills missing
              </p>
              <div className="gap-lists">
                <div className="matched-skills">
                  <h5>✅ Matched Skills ({candidate.skill_gaps.matched_skills.length})</h5>
                  <ul>
                    {candidate.skill_gaps.matched_skills.map((skill, i) => (
                      <li key={i} className="matched-item">{skill}</li>
                    ))}
                  </ul>
                </div>
                <div className="missing-skills">
                  <h5>❌ Missing Skills ({candidate.skill_gaps.missing_skills.length})</h5>
                  <ul>
                    {candidate.skill_gaps.missing_skills.map((skill, i) => (
                      <li key={i} className="missing-item">{skill}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ) : (
            <p className="success-message">✅ No skill gaps identified! Candidate matches all requirements.</p>
          )}
        </div>

        {/* Learning Roadmap */}
        {candidate.roadmap.roadmap && candidate.roadmap.roadmap.length > 0 && (
          <div className="detail-section">
            <h3>🗺️ Personalized Learning Roadmap</h3>
            <p className="roadmap-summary">
              <strong>Skills to Learn:</strong> {candidate.roadmap.total_skills_to_learn} | 
              <strong> Estimated Time:</strong> {candidate.roadmap.estimated_total_time}
            </p>
            
            <div className="roadmap-timeline">
              {candidate.roadmap.roadmap.map((item, index) => (
                <div key={index} className="roadmap-item">
                  <div className="roadmap-priority">Step {item.priority}</div>
                  <div className="roadmap-content">
                    <h4>{item.skill}</h4>
                    <p className="roadmap-time">⏱️ {item.estimated_time}</p>
                    
                    {item.milestones && (
                      <div className="milestones">
                        <strong>📍 Milestones:</strong>
                        <ul>
                          {item.milestones.map((milestone, i) => (
                            <li key={i}>{milestone}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    {item.resources && (
                      <div className="resources">
                        <strong>📚 Learning Resources:</strong>
                        {item.resources.beginner && (
                          <div className="resource-level">
                            <em>Beginner:</em>
                            <ul>
                              {item.resources.beginner.map((resource, i) => (
                                <li key={i}>{resource}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {item.resources.intermediate && (
                          <div className="resource-level">
                            <em>Intermediate:</em>
                            <ul>
                              {item.resources.intermediate.map((resource, i) => (
                                <li key={i}>{resource}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {item.resources.general && (
                          <div className="resource-level">
                            <ul>
                              {item.resources.general.map((resource, i) => (
                                <li key={i}>{resource}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Experience */}
        {candidate.experience && candidate.experience.length > 0 && (
          <div className="detail-section">
            <h3>💼 Experience</h3>
            <ul className="experience-list">
              {candidate.experience.map((exp, i) => (
                <li key={i}>{exp}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Education */}
        {candidate.education && candidate.education.length > 0 && (
          <div className="detail-section">
            <h3>🎓 Education</h3>
            <ul className="education-list">
              {candidate.education.map((edu, i) => (
                <li key={i}>{edu}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

// Helper functions
const getMaxScore = (key) => {
  const maxScores = {
    'contact_information': 15,
    'skills_section': 25,
    'experience_section': 20,
    'education_section': 15,
    'keyword_optimization': 15,
    'format_structure': 10
  };
  return maxScores[key] || 10;
};

const getScoreColor = (value, max) => {
  const percentage = (value / max) * 100;
  if (percentage >= 80) return '#4caf50';
  if (percentage >= 60) return '#8bc34a';
  if (percentage >= 40) return '#ff9800';
  return '#f44336';
};

export default RecruiterDashboard;
