from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class ExplainableAI:
    """Provide explanations for matching scores"""
    
    def explain_score(self, resume_text, job_description, match_score):
        """Generate explanation for the match score (backward compatible)"""
        return self.explain_score_with_bert(resume_text, job_description, match_score, None)
    
    def explain_score_with_bert(self, resume_text, job_description, match_score, matcher):
        """Enhanced explanation with BERT score breakdown"""
        
        if match_score >= 0.7:
            overall_assessment = "Excellent match"
            recommendation = "Highly recommended for interview"
        elif match_score >= 0.5:
            overall_assessment = "Good match"
            recommendation = "Recommended for interview"
        elif match_score >= 0.3:
            overall_assessment = "Moderate match"
            recommendation = "Consider with skill assessment"
        else:
            overall_assessment = "Weak match"
            recommendation = "Not recommended"
        
        # Get BERT score breakdown if available
        bert_breakdown = {}
        if matcher and hasattr(matcher, 'get_score_breakdown'):
            try:
                bert_breakdown = matcher.get_score_breakdown()
            except:
                bert_breakdown = {}
        
        # Get top matching sentences (BERT feature)
        top_sentences = []
        if matcher and hasattr(matcher, 'get_top_matching_sentences'):
            try:
                top_sentences = matcher.get_top_matching_sentences(resume_text, job_description, 3)
            except:
                top_sentences = []
        
        # Get keyword matches
        top_terms = []
        if matcher and hasattr(matcher, 'get_top_matching_terms'):
            try:
                top_terms_list = matcher.get_top_matching_terms(resume_text, job_description, 10)
                top_terms = [{'term': term, 'importance': 1.0} for term in top_terms_list[:5]]
            except:
                # Fallback to TF-IDF extraction
                top_terms = self._extract_tfidf_terms(resume_text, job_description)
        else:
            top_terms = self._extract_tfidf_terms(resume_text, job_description)
        
        return {
            'overall_assessment': overall_assessment,
            'recommendation': recommendation,
            'match_score_interpretation': self._interpret_score(match_score),
            'bert_breakdown': bert_breakdown,
            'top_contributing_terms': top_terms,
            'top_matching_sentences': top_sentences,
            'explanation': self._generate_textual_explanation_bert(match_score, top_sentences, bert_breakdown)
        }
    
    def _interpret_score(self, score):
        """Provide interpretation of the score"""
        score_pct = round(score * 100, 1)
        
        if score >= 0.7:
            return f"{score_pct}% match - Strong alignment with job requirements"
        elif score >= 0.5:
            return f"{score_pct}% match - Good alignment with most requirements"
        elif score >= 0.3:
            return f"{score_pct}% match - Partial alignment, some gaps exist"
        else:
            return f"{score_pct}% match - Limited alignment with requirements"
    
    def _generate_textual_explanation_bert(self, score, top_sentences, bert_breakdown):
        """Generate explanation with BERT insights"""
        explanation = ""
        
        if bert_breakdown and 'bert_semantic_score' in bert_breakdown:
            explanation += f"AI Analysis: BERT semantic matching score is {bert_breakdown.get('bert_semantic_score', 0)}% "
            explanation += f"with {bert_breakdown.get('skill_matching_score', 0)}% exact skill overlap. "
        
        if top_sentences and len(top_sentences) > 0:
            explanation += f"Most relevant resume section: '{top_sentences[0]['sentence'][:100]}...' "
        
        if score >= 0.6:
            explanation += "The candidate demonstrates strong relevant experience and skills with excellent semantic alignment."
        elif score >= 0.4:
            explanation += "The candidate has relevant experience but may lack some preferred qualifications."
        else:
            explanation += "The candidate has limited alignment with the core requirements."
        
        return explanation
    
    def _extract_tfidf_terms(self, resume_text, job_description):
        """Fallback TF-IDF term extraction"""
        try:
            vectorizer = TfidfVectorizer(max_features=100)
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
            
            feature_names = vectorizer.get_feature_names_out()
            resume_scores = tfidf_matrix[0].toarray()[0]
            jd_scores = tfidf_matrix[1].toarray()[0]
            
            contribution_scores = resume_scores * jd_scores
            top_indices = np.argsort(contribution_scores)[-10:][::-1]
            
            top_terms = [
                {
                    'term': feature_names[i],
                    'importance': round(float(contribution_scores[i]), 4)
                }
                for i in top_indices if contribution_scores[i] > 0
            ]
            
            return top_terms[:5]
        except:
            return []
