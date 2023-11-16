import clean_text
import pandas as pd

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def match_results(resume_text,job_descriptions):

    cleaned_resume = clean_text.clean_text_config(resume_text)

    # jobs_dataset = pd.read_csv('Jobs_posts.csv')
    job_descriptions['cleaned_description'] = job_descriptions['description'].apply(clean_text.clean_text_config)


    vectorizer = TfidfVectorizer()

    all_texts = [cleaned_resume] + job_descriptions['cleaned_description'].to_list()
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Kozin benzerliğini hesaplama
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Benzerlik skorlarını yazdırma
    job_match_scores = {f"Job {i+1}": score for i, score in enumerate(cosine_similarities)}
    # print(job_match_scores)
    job_descriptions['Match Scores'] = list(job_match_scores.values())
    return job_descriptions


# with open('example_resume.txt','r',encoding='utf-8') as f:
#     resume_text = f.read()

# job_post_dataset = pd.read_csv('Jobs_posts.csv')

# run = match_results(resume_text,job_post_dataset)
# print(run)