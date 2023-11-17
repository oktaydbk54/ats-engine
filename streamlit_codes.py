import streamlit as st
import read_pdfs
import pandas as pd
import requests
import json

api = 'http://localhost:8000/predict'

def main():
    st.title('Dream Job Finder')
    job_title = st.text_input('Please Enter Job Title')
    job_location = st.text_input('Please Enter Job Location')
    job_search_number = st.slider('Job Search Number?', 0, 20,5)
    
    resume_upload = st.file_uploader('Please Upload Resume/CV ', type='pdf')

    if job_title and job_location and job_search_number:
        with st.spinner(''):
            if resume_upload is not None:
                read_resume = read_pdfs.extract_text_from_pdf(resume_upload)
                #st.write(read_resume)
                st.write('Uploaded!')
            else:
                st.warning('Please Add Resume', icon="⚠️")
    
    if st.button('Start'):
        if job_title == '' or len(job_title) <= 4 or job_location == '':
            st.warning('Please Write Job Title or Job Location', icon="⚠️")
        
        feature_data = {
            'job_title':job_title,
            'job_location':job_location,
            'job_search_number':job_search_number,
            'resume':read_resume
        }

        headers = {'Content-Type':'application/json'}
        response = requests.post(url= api , data=json.dumps(feature_data),headers=headers)
        
        response_dataset = pd.DataFrame(response.json()['score'])
        response_dataset = response_dataset[['title','jobUrl','companyName','location','description','postedTime','Match Scores']]

        st.title('Prediction Results')        
        st.dataframe(response_dataset)
        st.write('Finished!')

if __name__ == "__main__":
    main()
