import React, { useState } from 'react';
import axios from 'axios';
import './StudentDashboard.css';

const StudentDashboard = () => {
  const [resume, setResume] = useState(null);
  const [targetRole, setTargetRole] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const roles = [
    'Software Engineer',
    'Data Scientist',
    'Full Stack Developer',
    'DevOps Engineer',
    'Frontend Developer'
  ];

  const handleFileChange = (e) => {
    setResume(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!resume) {
      alert('Please upload your resume');
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append('resume', resume);
    formData.append('target_role', targetRole);

    try {
      const response = await axios.post(
        'http://localhost:5000/api/analyze-single',
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );

      setResults(response.data);
      alert('Analysis completed!');
    } catch (error) {
      console.error('Error:', error);
      alert('Error analyzing resume: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="student-dashboard">
      <h2>👨‍🎓 Student Dashboard</h2>
      <p className="subtitle">Get AI-powered insights to improve your resume and career readiness</p>

      <div className="upload-section">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Upload Your Resume:</label>
            <input type="file" accept=".pdf,.docx" onChange={handleFileChange} />
            {resume && <p className="file-name">📄 {resume.name}</p>}
          </div>

          <div className="form-group">
            <label>Target Role (Optional):</label>
            <select value={targetRole} onChange={(e) => setTargetRole(e.target.value)}>
              <option value="">Select a role...</option>
              {roles.map(role => (
                <option key={role} value={role}>{role}</option>
              ))}
            </select>
          </div>

          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Analyzing...' : 'Analyze My Resume'}
          </button>
        </form>
      </div>

      {results && (
        <div className="analysis-results">
          {/* ATS Score Card */}
          <div className="score-card">
            <h3>Your ATS Score</h3>
            <div className="score-circle">
              <span className="score-value">{results.ats_score}</span>
              <span className="score-max">/100</span>
            </div>
            <p className="score-interpretation">
              {results.ats_score >= 80 ? '🎉 Excellent! Your resume is ATS-friendly' :
               results.ats_score >= 60 ? '✅ Good! Minor improvements needed' :
               results.ats_score >= 40 ? '⚠️ Fair - Needs improvement' :
               '❌ Poor - Significant changes needed'}
            </p>
          </div>

          {/* AI Insights - How to Improve */}
          <div className="insights-section">
            <h3>🤖 AI Insights - How to Increase Your Score</h3>
            <div className="insights-grid">
              {generateImprovementSuggestions(results.ats_breakdown, results.ats_score).map((suggestion, index) => (
                <div key={index} className={`insight-card ${suggestion.priority}`}>
                  <div className="insight-icon">{suggestion.icon}</div>
                  <h4>{suggestion.title}</h4>
                  <p>{suggestion.description}</p>
                  <div className="insight-impact">Impact: {suggestion.impact}</div>
                </div>
              ))}
            </div>
          </div>

          {/* ATS Breakdown */}
          <div className="breakdown-section">
            <h3>📊 Detailed ATS Score Breakdown</h3>
            {Object.entries(results.ats_breakdown).map(([key, value]) => (
              <div key={key} className="breakdown-item">
                <div className="breakdown-header">
                  <span className="breakdown-label">
                    {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </span>
                  <span className="breakdown-score">{value}/{getMaxScore(key)}</span>
                </div>
                <div className="breakdown-bar">
                  <div 
                    className="breakdown-fill" 
                    style={{
                      width: `${(value / getMaxScore(key)) * 100}%`,
                      backgroundColor: getScoreColor(value, getMaxScore(key))
                    }}
                  ></div>
                </div>
                <p className="breakdown-tip">{getTipForCategory(key, value, getMaxScore(key))}</p>
              </div>
            ))}
          </div>

          {/* Extracted Information */}
          <div className="info-section">
            <h3>📋 Extracted Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <strong>Name:</strong> {results.candidate_data.name}
              </div>
              <div className="info-item">
                <strong>Email:</strong> {results.candidate_data.email}
              </div>
              <div className="info-item">
                <strong>Phone:</strong> {results.candidate_data.phone}
              </div>
              <div className="info-item">
                <strong>Skills Found:</strong> {results.candidate_data.skills.length}
              </div>
            </div>
          </div>

          {/* Skills */}
          <div className="skills-section">
            <h3>💡 Your Skills ({results.candidate_data.skills.length})</h3>
            <div className="skills-grid">
              {results.candidate_data.skills.map((skill, i) => (
                <span key={i} className="skill-badge">{skill}</span>
              ))}
            </div>
          </div>

          {/* Skill Gaps & Roadmap */}
          {targetRole && results.skill_gaps.readiness_score !== undefined && (
            <>
              <div className="readiness-section">
                <h3>🎯 Career Readiness for {targetRole}</h3>
                <div className="readiness-meter">
                  <div className="readiness-bar">
                    <div 
                      className="readiness-fill" 
                      style={{width: `${results.skill_gaps.readiness_score}%`}}
                    >
                      {results.skill_gaps.readiness_score}%
                    </div>
                  </div>
                  <p className="readiness-label">
                    {results.skill_gaps.readiness_score >= 80 ? '🎉 You\'re ready!' :
                     results.skill_gaps.readiness_score >= 60 ? '💪 Almost there!' :
                     results.skill_gaps.readiness_score >= 40 ? '📚 Keep learning!' :
                     '🚀 Start your journey!'}
                  </p>
                </div>
              </div>

              <div className="gaps-section">
                <h3>📉 Skill Gap Analysis</h3>
                
                {results.skill_gaps.missing_required && results.skill_gaps.missing_required.length > 0 && (
                  <div className="gap-category critical">
                    <h4>❌ Missing Required Skills (Critical)</h4>
                    <ul>
                      {results.skill_gaps.missing_required.map((skill, i) => (
                        <li key={i}>{skill}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {results.skill_gaps.missing_preferred && results.skill_gaps.missing_preferred.length > 0 && (
                  <div className="gap-category preferred">
                    <h4>⚡ Missing Preferred Skills (Recommended)</h4>
                    <ul>
                      {results.skill_gaps.missing_preferred.map((skill, i) => (
                        <li key={i}>{skill}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {results.skill_gaps.matched_required && results.skill_gaps.matched_required.length > 0 && (
                  <div className="gap-category matched">
                    <h4>✅ Skills You Already Have</h4>
                    <ul>
                      {results.skill_gaps.matched_required.map((skill, i) => (
                        <li key={i}>{skill}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Learning Roadmap */}
              {results.roadmap.roadmap && results.roadmap.roadmap.length > 0 && (
                <div className="roadmap-section">
                  <h3>🗺️ Your Personalized Learning Roadmap</h3>
                  <p className="roadmap-intro">
                    Follow this AI-generated roadmap to become job-ready for <strong>{targetRole}</strong>
                  </p>
                  <div className="roadmap-stats">
                    <div className="stat-item">
                      <div className="stat-value">{results.roadmap.total_skills_to_learn}</div>
                      <div className="stat-label">Skills to Learn</div>
                    </div>
                    <div className="stat-item">
                      <div className="stat-value">{results.roadmap.estimated_total_time}</div>
                      <div className="stat-label">Estimated Time</div>
                    </div>
                  </div>

                  <div className="roadmap-timeline">
                    {results.roadmap.roadmap.map((item, index) => (
                      <div key={index} className="roadmap-card">
                        <div className="roadmap-badge">Step {item.priority}</div>
                        <div className="roadmap-details">
                          <h4>{item.skill}</h4>
                          <p className="roadmap-duration">⏱️ {item.estimated_time}</p>
                          
                          {item.milestones && (
                            <div className="roadmap-milestones">
                              <strong>📍 Learning Path:</strong>
                              <ul>
                                {item.milestones.map((milestone, i) => (
                                  <li key={i}>{milestone}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                          
                          {item.resources && (
                            <div className="roadmap-resources">
                              <strong>📚 Recommended Resources:</strong>
                              {item.resources.beginner && (
                                <div className="resource-tier">
                                  <span className="tier-label">Beginner</span>
                                  <ul>
                                    {item.resources.beginner.map((resource, i) => (
                                      <li key={i}>{resource}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                              {item.resources.intermediate && (
                                <div className="resource-tier">
                                  <span className="tier-label">Intermediate</span>
                                  <ul>
                                    {item.resources.intermediate.map((resource, i) => (
                                      <li key={i}>{resource}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                              {item.resources.general && (
                                <div className="resource-tier">
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
            </>
          )}
        </div>
      )}
    </div>
  );
};

// Helper Functions
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

const getTipForCategory = (category, value, max) => {
  const percentage = (value / max) * 100;
  
  const tips = {
    'contact_information': {
      high: '✅ Great! Your contact info is complete and ATS-friendly.',
      medium: '⚠️ Add missing contact details (email, phone, or name).',
      low: '❌ Critical: Add proper contact information at the top of your resume.'
    },
    'skills_section': {
      high: '✅ Excellent skill keywords! Well-optimized for ATS.',
      medium: '⚠️ Add 5-10 more relevant technical skills.',
      low: '❌ Add a dedicated Skills section with 10+ relevant keywords.'
    },
    'experience_section': {
      high: '✅ Strong work experience section!',
      medium: '⚠️ Add more experience entries or detail.',
      low: '❌ Add work experience with dates and achievements.'
    },
    'education_section': {
      high: '✅ Education section is complete.',
      medium: '⚠️ Ensure degree, institution, and year are included.',
      low: '❌ Add your education details (degree and institution).'
    },
    'keyword_optimization': {
      high: '✅ Great use of action verbs and keywords!',
      medium: '⚠️ Use more action verbs (developed, managed, led, etc.).',
      low: '❌ Add action verbs and achievements with metrics.'
    },
    'format_structure': {
      high: '✅ Well-structured and formatted resume!',
      medium: '⚠️ Improve formatting and section organization.',
      low: '❌ Restructure with clear sections and better formatting.'
    }
  };
  
  if (percentage >= 80) return tips[category].high;
  if (percentage >= 50) return tips[category].medium;
  return tips[category].low;
};

const generateImprovementSuggestions = (breakdown, totalScore) => {
  const suggestions = [];
  
  Object.entries(breakdown).forEach(([key, value]) => {
    const max = getMaxScore(key);
    const percentage = (value / max) * 100;
    
    if (percentage < 70) {
      let suggestion = null;
      
      if (key === 'skills_section' && percentage < 70) {
        suggestion = {
          icon: '💡',
          title: 'Add More Skills',
          description: 'Include 10-15 relevant technical skills. Use exact keywords from job descriptions.',
          impact: 'High',
          priority: 'high'
        };
      } else if (key === 'keyword_optimization' && percentage < 70) {
        suggestion = {
          icon: '📝',
          title: 'Use Action Verbs',
          description: 'Start bullet points with strong action verbs like "Developed", "Led", "Implemented", "Achieved".',
          impact: 'High',
          priority: 'high'
        };
      } else if (key === 'experience_section' && percentage < 70) {
        suggestion = {
          icon: '💼',
          title: 'Expand Experience',
          description: 'Add 2-3 more experience entries with quantifiable achievements and dates.',
          impact: 'Medium',
          priority: 'medium'
        };
      } else if (key === 'format_structure' && percentage < 70) {
        suggestion = {
          icon: '📄',
          title: 'Improve Formatting',
          description: 'Use clear section headings, consistent fonts, and bullet points. Aim for 400-600 words.',
          impact: 'Medium',
          priority: 'medium'
        };
      } else if (key === 'contact_information' && percentage < 70) {
        suggestion = {
          icon: '📧',
          title: 'Complete Contact Info',
          description: 'Add your full name, professional email, and phone number at the top.',
          impact: 'Critical',
          priority: 'critical'
        };
      }
      
      if (suggestion) suggestions.push(suggestion);
    }
  });
  
  // Add general suggestions
  if (totalScore < 60) {
    suggestions.push({
      icon: '🎯',
      title: 'Tailor to Job Description',
      description: 'Customize your resume for each job by matching keywords from the job posting.',
      impact: 'Very High',
      priority: 'high'
    });
  }
  
  if (suggestions.length === 0) {
    suggestions.push({
      icon: '🎉',
      title: 'Great Job!',
      description: 'Your resume is well-optimized. Keep updating it with new skills and achievements.',
      impact: 'Maintenance',
      priority: 'low'
    });
  }
  
  return suggestions.slice(0, 6); // Show top 6 suggestions
};

export default StudentDashboard;
