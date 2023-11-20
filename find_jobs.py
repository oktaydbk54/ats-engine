from apify_client import ApifyClient
import pandas as pd

def send_requests_for_job_post(job_title,job_location,job_search_number):

    client = ApifyClient("apify_api_XaCM2BtiX2y80sFxZqcL2H3SpuUJmK4fhfXw")

    run_input = {
        "title": job_title,
        "location": job_location,
        "rows": job_search_number,
    }

    run = client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)

    jobs_list = list()
    count = 0
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        jobs_list.append(item)
        count += 1
        if count == int(job_search_number):
            break
    jobs_dataset = pd.DataFrame(jobs_list)
    # jobs_dataset.to_csv(f'Sample_job_posts/{job_title}_{job_location}Jobs_posts.csv',index=False)
    return jobs_dataset

