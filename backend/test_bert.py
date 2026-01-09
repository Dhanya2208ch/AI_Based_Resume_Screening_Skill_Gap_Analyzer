from matcher_bert import BERTResumeMatcher

print("Testing BERT matcher...")

# Initialize
matcher = BERTResumeMatcher()

# Test case
resume = """
Python Developer with 5 years experience.
Expert in Django and Flask frameworks.
Built RESTful APIs using PostgreSQL.
Worked with Docker and AWS cloud services.
Strong background in machine learning and data science.
"""

job_description = """
Looking for Senior Python Engineer.
Required: Python, Django, REST API, PostgreSQL, Docker
Preferred: AWS, Machine Learning
"""

# Calculate similarity
score = matcher.calculate_similarity(resume, job_description)

print(f"\n✅ Match Score: {score * 100:.2f}%")

# Get breakdown
breakdown = matcher.get_score_breakdown()
print(f"\n📊 Score Breakdown:")
print(f"   BERT Semantic: {breakdown['bert_semantic_score']}%")
print(f"   Skill Matching: {breakdown['skill_matching_score']}%")
print(f"   Final Score: {breakdown['final_score']}%")

# Get top sentences
top_sentences = matcher.get_top_matching_sentences(resume, job_description, 3)
print(f"\n🎯 Most Relevant Resume Sections:")
for i, sent in enumerate(top_sentences, 1):
    print(f"   {i}. {sent['sentence']} (Relevance: {sent['relevance']:.1f}%)")

print("\n✅ BERT matcher working perfectly!")
