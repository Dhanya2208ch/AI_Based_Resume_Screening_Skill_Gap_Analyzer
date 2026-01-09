from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

from resume_parser import ResumeParser
from skill_extractor import SkillExtractor
from matcher_bert import BERTResumeMatcher
from skill_gap_analyzer import SkillGapAnalyzer
from roadmap_generator import RoadmapGenerator
from explainer import ExplainableAI
from ats_scorer import ATSScorer

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
resume_parser = ResumeParser()
skill_extractor = SkillExtractor()
matcher = BERTResumeMatcher()
skill_gap_analyzer = SkillGapAnalyzer()
roadmap_generator = RoadmapGenerator()
explainer = ExplainableAI()
ats_scorer = ATSScorer()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload-resumes', methods=['POST'])
def upload_resumes():
    """Upload multiple resumes and job description"""
    try:
        if 'resumes' not in request.files:
            return jsonify({'error': 'No resumes provided'}), 400
        
        job_description = request.form.get('job_description', '')
        if not job_description:
            return jsonify({'error': 'Job description required'}), 400
        
        files = request.files.getlist('resumes')
        results = []
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Process resume
                resume_text = resume_parser.extract_text(filepath)
                candidate_data = skill_extractor.extract_candidate_info(resume_text)
                match_score = matcher.calculate_similarity(resume_text, job_description)
                ats_score, ats_breakdown = ats_scorer.calculate_ats_score(resume_text, candidate_data)
                skill_gaps = skill_gap_analyzer.identify_gaps(candidate_data['skills'], job_description)
                roadmap = roadmap_generator.generate_roadmap(skill_gaps)
                explanation = explainer.explain_score_with_bert(resume_text, job_description, match_score, matcher)
                
                results.append({
                    'filename': filename,
                    'candidate_name': candidate_data.get('name', 'Unknown'),
                    'email': candidate_data.get('email', 'N/A'),
                    'phone': candidate_data.get('phone', 'N/A'),
                    'skills': candidate_data.get('skills', []),
                    'experience': candidate_data.get('experience', []),
                    'education': candidate_data.get('education', []),
                    'match_score': round(match_score * 100, 2),
                    'ats_score': round(ats_score, 2),
                    'ats_breakdown': ats_breakdown,
                    'skill_gaps': skill_gaps,
                    'roadmap': roadmap,
                    'explanation': explanation
                })
                
                os.remove(filepath)  # Clean up
        
        results.sort(key=lambda x: x['match_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'candidates': results,
            'total_candidates': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-single', methods=['POST'])
def analyze_single():
    """Analyze single resume for student dashboard"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume provided'}), 400
        
        file = request.files['resume']
        target_role = request.form.get('target_role', '')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            resume_text = resume_parser.extract_text(filepath)
            candidate_data = skill_extractor.extract_candidate_info(resume_text)
            ats_score, ats_breakdown = ats_scorer.calculate_ats_score(resume_text, candidate_data)
            
            if target_role:
                skill_gaps = skill_gap_analyzer.identify_gaps_by_role(candidate_data['skills'], target_role)
                roadmap = roadmap_generator.generate_roadmap(skill_gaps)
            else:
                skill_gaps = []
                roadmap = []
            
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'candidate_data': candidate_data,
                'ats_score': round(ats_score, 2),
                'ats_breakdown': ats_breakdown,
                'skill_gaps': skill_gaps,
                'roadmap': roadmap
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'Backend running successfully!'}), 200

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, port=5000)
