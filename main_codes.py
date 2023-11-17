from fastapi import FastAPI, HTTPException
import find_jobs
import clean_text
import calculate_score
import calculate_score_v2
import calculate_score_v3
import json
from pydantic import BaseModel

app = FastAPI()

class PredictRequest(BaseModel):
    job_title: str
    job_location: str
    job_search_number: float
    resume: str

@app.post("/predict")
async def predict(request: PredictRequest):
    
    try:
        job_title = request.job_title
        job_location = request.job_location
        job_search_number = request.job_search_number
        resume = request.resume

        # İş açıklamalarını bul
        job_descriptions = find_jobs.send_requests_for_job_post(job_title, job_location,job_search_number)

        # Eşleşme skorunu hesapla
        # score = calculate_score.match_results(resume, job_descriptions)
        # score = calculate_score_v2.match_results(resume, job_descriptions)
        score = calculate_score_v3.match_results(resume, job_descriptions)

        # Sonucu geri gönder
        return {"score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
