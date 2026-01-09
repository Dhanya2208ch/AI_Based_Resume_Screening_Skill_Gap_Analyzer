class SkillGapAnalyzer:
    """Identify skill gaps between candidate and job requirements"""
    
    def __init__(self):
        self.role_skills = {
            'software engineer': {
                'required': ['python', 'java', 'git', 'sql', 'data structures'],
                'preferred': ['docker', 'kubernetes', 'aws', 'react', 'node.js']
            },
            'data scientist': {
                'required': ['python', 'machine learning', 'pandas', 'numpy', 'sql'],
                'preferred': ['tensorflow', 'pytorch', 'deep learning', 'nlp', 'tableau']
            },
            'full stack developer': {
                'required': ['javascript', 'react', 'node.js', 'sql', 'html', 'css'],
                'preferred': ['mongodb', 'express', 'docker', 'aws', 'typescript']
            },
            'devops engineer': {
                'required': ['docker', 'kubernetes', 'jenkins', 'git', 'linux'],
                'preferred': ['terraform', 'ansible', 'aws', 'python']
            },
            'frontend developer': {
                'required': ['javascript', 'html', 'css', 'react'],
                'preferred': ['typescript', 'webpack', 'sass']
            }
        }
    
    def identify_gaps(self, candidate_skills, job_description):
        """Identify missing skills from job description"""
        jd_lower = job_description.lower()
        required_skills = []
        
        skill_patterns = ['python', 'java', 'javascript', 'react', 'angular', 'vue',
                         'node.js', 'django', 'flask', 'sql', 'mongodb', 'aws',
                         'docker', 'kubernetes', 'machine learning', 'deep learning']
        
        for skill in skill_patterns:
            if skill in jd_lower:
                required_skills.append(skill)
        
        candidate_skills_lower = [skill.lower() for skill in candidate_skills]
        missing_skills = [skill for skill in required_skills 
                         if skill not in candidate_skills_lower]
        
        return {
            'missing_skills': missing_skills,
            'matched_skills': [skill for skill in required_skills 
                             if skill in candidate_skills_lower],
            'gap_percentage': round((len(missing_skills) / len(required_skills) * 100) 
                                   if required_skills else 0, 2)
        }
    
    def identify_gaps_by_role(self, candidate_skills, target_role):
        """Identify gaps based on predefined role requirements"""
        role_lower = target_role.lower()
        
        if role_lower not in self.role_skills:
            return {'error': 'Role not found'}
        
        requirements = self.role_skills[role_lower]
        candidate_skills_lower = [skill.lower() for skill in candidate_skills]
        
        missing_required = [skill for skill in requirements['required'] 
                           if skill not in candidate_skills_lower]
        missing_preferred = [skill for skill in requirements['preferred'] 
                            if skill not in candidate_skills_lower]
        
        return {
            'role': target_role,
            'missing_required': missing_required,
            'missing_preferred': missing_preferred,
            'matched_required': [skill for skill in requirements['required'] 
                                if skill in candidate_skills_lower],
            'readiness_score': round(
                (len(requirements['required']) - len(missing_required)) / 
                len(requirements['required']) * 100, 2
            )
        }
