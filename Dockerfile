FROM python:3.11-slim

WORKDIR /source

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

# Print the files in the current directory during the build
RUN echo "Listing files in $PWD:" && ls -alh

ENV PYTHONUNBUFFERED=1 \ 
    PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "src.app.server:app", "--host", "0.0.0.0", "--port", "8000"]