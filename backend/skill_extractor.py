import spacy
import re

class SkillExtractor:
    """Extract structured information from resume text using NLP"""
    
    def __init__(self):
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Comprehensive skill database
        self.skill_keywords = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 
                          'php', 'swift', 'kotlin', 'typescript', 'go', 'rust', 
                          'r', 'matlab', 'sql', 'scala', 'perl', 'shell scripting'],
            'web_development': ['react', 'angular', 'vue', 'node.js', 'express', 
                              'django', 'flask', 'spring', 'html', 'css', 'sass',
                              'webpack', 'next.js', 'asp.net', 'laravel'],
            'data_science': ['machine learning', 'deep learning', 'nlp', 'tensorflow',
                           'pytorch', 'keras', 'pandas', 'numpy', 'scikit-learn',
                           'data analysis', 'statistical modeling'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle',
                        'sql server', 'dynamodb', 'cassandra', 'elasticsearch'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
                     'terraform', 'ansible', 'ci/cd', 'devops'],
            'tools': ['git', 'github', 'jira', 'confluence', 'visual studio',
                     'vs code', 'postman', 'tableau', 'power bi'],
            'soft_skills': ['communication', 'leadership', 'teamwork', 'problem solving',
                          'analytical thinking', 'project management', 'agile', 'scrum']
        }
        
        # Flatten all skills
        self.all_skills = []
        for category, skills in self.skill_keywords.items():
            self.all_skills.extend(skills)
    
    def extract_candidate_info(self, resume_text):
        """Extract name, email, phone, skills, experience, education"""
        doc = self.nlp(resume_text)
        
        return {
            'name': self._extract_name(doc, resume_text),
            'email': self._extract_email(resume_text),
            'phone': self._extract_phone(resume_text),
            'skills': self._extract_skills(resume_text),
            'experience': self._extract_experience(doc, resume_text),
            'education': self._extract_education(doc, resume_text)
        }
    
    def _extract_name(self, doc, text):
        """Extract candidate name using NER"""
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                return ent.text
        
        # Fallback: assume first line is name
        lines = text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if line and len(line.split()) >= 2 and len(line) < 50:
                return line
        
        return "Unknown"
    
    def _extract_email(self, text):
        """Extract email using regex"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else "N/A"
    
    def _extract_phone(self, text):
        """Extract phone number using regex"""
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else "N/A"
    
    def _extract_skills(self, text):
        """Extract technical and soft skills"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.all_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        return list(set(found_skills))
    
    def _extract_experience(self, doc, text):
        """Extract work experience sections"""
        experience = []
        lines = text.split('\n')
        
        exp_keywords = ['experience', 'work history', 'employment']
        in_experience_section = False
        
        for line in lines:
            line_lower = line.lower().strip()
            
            if any(keyword in line_lower for keyword in exp_keywords):
                in_experience_section = True
                continue
            
            if in_experience_section and any(keyword in line_lower for keyword in 
                                            ['education', 'skills', 'projects']):
                break
            
            if in_experience_section and line.strip():
                date_pattern = r'\b(19|20)\d{2}\b'
                if re.search(date_pattern, line):
                    experience.append(line.strip())
        
        return experience[:5]
    
    def _extract_education(self, doc, text):
        """Extract education information"""
        education = []
        lines = text.split('\n')
        
        edu_keywords = ['education', 'academic', 'qualification']
        degree_keywords = ['b.tech', 'b.e.', 'm.tech', 'm.s.', 'mba', 'phd', 
                          'bachelor', 'master', 'diploma']
        
        in_education_section = False
        
        for line in lines:
            line_lower = line.lower().strip()
            
            if any(keyword in line_lower for keyword in edu_keywords):
                in_education_section = True
                continue
            
            if in_education_section and any(keyword in line_lower for keyword in 
                                           ['experience', 'skills', 'projects']):
                break
            
            if in_education_section and any(degree in line_lower for degree in degree_keywords):
                education.append(line.strip())
        
        return education[:3]
