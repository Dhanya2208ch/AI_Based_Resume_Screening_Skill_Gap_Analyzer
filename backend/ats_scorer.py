import re

class ATSScorer:
    """Calculate ATS compatibility score"""
    
    def calculate_ats_score(self, resume_text, candidate_data):
        """Calculate comprehensive ATS score"""
        scores = {}
        
        scores['contact_information'] = self._score_contact_info(candidate_data)
        scores['skills_section'] = self._score_skills(candidate_data['skills'])
        scores['experience_section'] = self._score_experience(candidate_data['experience'])
        scores['education_section'] = self._score_education(candidate_data['education'])
        scores['keyword_optimization'] = self._score_keywords(resume_text)
        scores['format_structure'] = self._score_format(resume_text)
        
        total_score = sum(scores.values())
        
        return total_score, scores
    
    def _score_contact_info(self, candidate_data):
        score = 0
        if candidate_data.get('name') and candidate_data['name'] != 'Unknown':
            score += 5
        if candidate_data.get('email') and candidate_data['email'] != 'N/A':
            score += 5
        if candidate_data.get('phone') and candidate_data['phone'] != 'N/A':
            score += 5
        return score
    
    def _score_skills(self, skills):
        if len(skills) == 0:
            return 0
        elif len(skills) < 5:
            return 10
        elif len(skills) < 10:
            return 18
        else:
            return 25
    
    def _score_experience(self, experience):
        if len(experience) == 0:
            return 0
        elif len(experience) == 1:
            return 10
        elif len(experience) <= 3:
            return 15
        else:
            return 20
    
    def _score_education(self, education):
        return 15 if len(education) >= 1 else 0
    
    def _score_keywords(self, resume_text):
        important_keywords = ['led', 'managed', 'developed', 'improved', 
                             'achieved', 'designed', 'implemented', 'created']
        
        text_lower = resume_text.lower()
        keyword_count = sum(1 for keyword in important_keywords if keyword in text_lower)
        
        if keyword_count >= 8:
            return 15
        elif keyword_count >= 5:
            return 10
        elif keyword_count >= 3:
            return 5
        return 0
    
    def _score_format(self, resume_text):
        score = 10
        word_count = len(resume_text.split())
        if word_count < 200 or word_count > 1500:
            score -= 3
        return max(0, score)
