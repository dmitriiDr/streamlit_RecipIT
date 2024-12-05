FROM python:3.8-slim
# Set the working directory
WORKDIR /app
# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt --verbose

COPY . .
COPY templates /app/templates
COPY database /app/database
COPY utils /app/utils
COPY configs /app/configs


# Expose port
EXPOSE 8501


# Command to run the Flask app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]