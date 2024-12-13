# Untuk deployment ke Cloud Run
# Gunakan image Python
FROM python:3.8-slim

# Set working directory di container
WORKDIR /app

# Salin requirements.txt ke dalam container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh file ke dalam container
COPY . /app/

# Set port yang akan digunakan
EXPOSE 8080

# Tentukan command untuk menjalankan aplikasi
CMD ["python", "app.py"]
