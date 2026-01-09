from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

class ResumeMatcher:
    """Calculate similarity between resumes and job descriptions"""
    
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            nltk.download('punkt')
            self.stop_words = set(stopwords.words('english'))
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words]
        return ' '.join(tokens)
    
    def calculate_similarity(self, resume_text, job_description):
        """Calculate cosine similarity using TF-IDF"""
        resume_processed = self.preprocess_text(resume_text)
        jd_processed = self.preprocess_text(job_description)
        
        vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([resume_processed, jd_processed])
        
        similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return similarity_score
    
    def get_top_matching_terms(self, resume_text, job_description, top_n=10):
        """Get top matching keywords"""
        resume_processed = self.preprocess_text(resume_text)
        jd_processed = self.preprocess_text(job_description)
        
        vectorizer = TfidfVectorizer(max_features=500)
        tfidf_matrix = vectorizer.fit_transform([resume_processed, jd_processed])
        
        feature_names = vectorizer.get_feature_names_out()
        resume_scores = tfidf_matrix[0].toarray()[0]
        jd_scores = tfidf_matrix[1].toarray()[0]
        
        intersection_scores = resume_scores * jd_scores
        top_indices = np.argsort(intersection_scores)[-top_n:][::-1]
        top_terms = [(feature_names[i], intersection_scores[i]) for i in top_indices]
        
        return [term for term, score in top_terms if score > 0]
