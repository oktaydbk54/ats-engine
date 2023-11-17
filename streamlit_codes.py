import streamlit as st
import read_pdfs
import pandas as pd
import requests
import json

api = 'http://localhost:8000/predict'

def shorten_url(url):
    return f'<a href="{url}" target="_blank">apply</a>'

def main():
    st.title('ATS Engine')
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
        response_dataset = response_dataset[['title','jobUrl','companyName','location','postedTime','Match Scores']]
        response_dataset['jobUrl'] = response_dataset['jobUrl'].apply(shorten_url)
        response_dataset = response_dataset.sort_values(by=['Match Scores'], ascending=False)

        st.title('Prediction Results')        
        st.write(response_dataset.to_html(escape=False), unsafe_allow_html=True)
        st.write('Finished!')
    # Yeni eklenen imza kısmı
    st.markdown('**Credit By:** [Emincan Yılmaz](https://www.linkedin.com/in/emincan-yilmaz/) & [Boran Oktay Dabak](https://www.linkedin.com/in/boran-oktay-dabak/)')

if __name__ == "__main__":
    main()
