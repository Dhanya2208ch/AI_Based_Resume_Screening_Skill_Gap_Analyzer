class RoadmapGenerator:
    """Generate personalized learning roadmap"""
    
    def __init__(self):
        self.learning_resources = {
            'python': {
                'beginner': ['Python for Everybody (Coursera)', 
                           'Codecademy Python Course'],
                'intermediate': ['Real Python Tutorials', 
                               'Effective Python by Brett Slatkin'],
            },
            'machine learning': {
                'beginner': ['Andrew Ng ML Course (Coursera)',
                           'Hands-On Machine Learning (Book)'],
                'intermediate': ['Fast.ai Courses', 'Kaggle Competitions'],
            },
            'react': {
                'beginner': ['React Official Tutorial', 'Scrimba React Course'],
                'intermediate': ['React - The Complete Guide (Udemy)'],
            },
            'docker': {
                'beginner': ['Docker for Beginners (YouTube)', 'Docker Docs'],
                'intermediate': ['Docker Deep Dive', 'Docker Compose Tutorial'],
            },
            'sql': {
                'beginner': ['SQL Basics (W3Schools)', 'SQLBolt Tutorial'],
                'intermediate': ['Mode SQL Tutorial', 'Advanced SQL Queries'],
            }
        }
    
    def generate_roadmap(self, skill_gaps):
        """Generate step-by-step learning roadmap"""
        missing_skills = skill_gaps.get('missing_skills', [])
        
        if not missing_skills:
            return {'message': 'No skill gaps!', 'roadmap': []}
        
        roadmap = []
        
        for i, skill in enumerate(missing_skills, 1):
            skill_lower = skill.lower()
            
            if skill_lower in self.learning_resources:
                resources = self.learning_resources[skill_lower]
                roadmap.append({
                    'priority': i,
                    'skill': skill,
                    'estimated_time': self._estimate_time(skill_lower),
                    'resources': resources,
                    'milestones': self._get_milestones(skill_lower)
                })
            else:
                roadmap.append({
                    'priority': i,
                    'skill': skill,
                    'estimated_time': '4-8 weeks',
                    'resources': {
                        'general': [f'{skill} tutorial on YouTube',
                                   f'Official {skill} documentation']
                    },
                    'milestones': ['Learn basics', 'Build project']
                })
        
        return {
            'total_skills_to_learn': len(missing_skills),
            'estimated_total_time': f'{len(missing_skills) * 6} weeks',
            'roadmap': roadmap
        }
    
    def _estimate_time(self, skill):
        time_estimates = {
            'python': '6-8 weeks',
            'javascript': '6-8 weeks',
            'react': '4-6 weeks',
            'machine learning': '8-12 weeks',
            'docker': '3-4 weeks',
            'sql': '4-6 weeks'
        }
        return time_estimates.get(skill, '4-8 weeks')
    
    def _get_milestones(self, skill):
        milestones = {
            'python': ['Complete syntax', 'Build 3 projects', 'Learn OOP'],
            'react': ['Understand Components', 'Master Hooks', 'Build App'],
            'machine learning': ['ML basics', 'Implement algorithms', 'Deploy model']
        }
        return milestones.get(skill, ['Learn basics', 'Build project'])
