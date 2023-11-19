# Use a Python 3.8 base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Clone the repository
RUN git clone https://github.com/oktaydbk54/ats-engine /app

# Install Python dependencies from requirements.txt


# Expose ports for Streamlit and FastAPI
EXPOSE 8501
EXPOSE 8000

# Install Supervisor for managing multiple processes
RUN apt-get update && apt-get install -y supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN pip install -r /app/requirements.txt
CMD ["/usr/bin/supervisord"]
CMD ["streamlit", "run", "/app/streamlit_codes.py"]
CMD ["uvicorn", "main_codes:app", "--host", "0.0.0.0", "--port", "8000"]
