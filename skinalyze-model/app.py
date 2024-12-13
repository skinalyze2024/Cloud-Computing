# File utama untuk API Flask
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io

# Inisialisasi Flask
app = Flask(__name__)

# Memuat model
model = load_model('Skinalyze.h5')

# Daftar nama penyakit sesuai dengan urutan kelas model
penyakit_classes = [
    "acne", "carcinoma", "herpes", "milia", "nail fungus", "normal", "vitiligo"
]

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'Upss, Kamu belum upload foto ya!'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Upss, Kamu belum upload foto ya!'}), 400

    # Membaca gambar dari file yang diupload
    img = Image.open(io.BytesIO(file.read()))
    img = img.resize((224, 224))  
    img_array = np.array(img) / 255.0  
    img_array = np.expand_dims(img_array, axis=0)  

    # Prediksi menggunakan model
    prediction = model.predict(img_array)
    
    # Menentukan kelas penyakit berdasarkan hasil prediksi
    predicted_class_index = np.argmax(prediction)  # Mengambil index kelas dengan probabilitas tertinggi
    predicted_class = penyakit_classes[predicted_class_index]
    confidence = prediction[0][predicted_class_index]  # Confidence dari model untuk prediksi ini

    # Membuat pesan sesuai dengan hasil prediksi berdasarkan confidence
        # Membuat pesan sesuai dengan hasil prediksi berdasarkan confidence
    if predicted_class == "normal":
        message = "Kulit terlihat normal dan sehat. Tidak terindikasi penyakit. Tetap jaga kesehatan kulitmu ya!"
    elif confidence <= 0.4:
        message = f"Risiko terkena penyakit sangat kecil. Aman kok, stay safe ya!!!"
    elif 0.4 < confidence <= 0.6:
        message = f"Kemungkinan terkena penyakit {predicted_class} ada, tetapi masih belum terlalu signifikan. Pertimbangkan untuk konsultasi ke dokter yaa."
    else:  # confidence > 0.6
        message = f"Ya, kamu terindikasi terkena penyakit {predicted_class} dengan tingkat keyakinan yang tinggi. Disarankan segera memeriksakan diri ke dokter."


    # Kembalikan hasil prediksi dan pesan sebagai JSON
    return jsonify({
        'prediction': predicted_class,
        'confidence': float(confidence),
        'message': message
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)



# Code GCP
# import tensorflow as tf
# from tensorflow.lite.python.interpreter import Interpreter
# from flask import Flask, request, jsonify
# from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
# import numpy as np
# from PIL import Image
# import io
# from google.cloud import storage
# import tempfile

# app = Flask(__name__)

# # Konfigurasi untuk JWT
# app.config['JWT_SECRET_KEY'] = 'my_super_secret_key_12345'  # Gunakan kunci yang sama dengan yang digunakan di >
# jwt = JWTManager(app)

# # Inisialisasi Google Cloud Storage client
# client = storage.Client()

# # Nama bucket dan path model di GCS
# bucket_name = "skinalyze-model"
# model_path = "Skinalyze.tflite"  # Ubah ke nama model TFLite Anda

# # Fungsi untuk mengunduh model dari GCS (Cukup dipanggil sekali saat aplikasi dimulai)
# def download_model_from_gcs(bucket_name, model_path):
#     try:
#         bucket = client.get_bucket(bucket_name)
#         blob = bucket.blob(model_path)
#         # Menyimpan model ke file sementara
#         with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#             blob.download_to_filename(temp_file.name)
#             return temp_file.name
#     except Exception as e:
#         print(f"Error downloading model from GCS: {e}")
#         return None
#     # Mengunduh dan memuat model dari GCS sekali saat aplikasi dimulai
# model_file = download_model_from_gcs(bucket_name, model_path)
# if model_file:
#     try:
#         # Memuat model TFLite
#         interpreter = Interpreter(model_path=model_file)
#         interpreter.allocate_tensors()
#         print("TFLite model successfully loaded!")
#     except Exception as e:
#         print(f"Error loading model: {e}")
# else:
#     print("Model file could not be downloaded from GCS.")

# # Daftar nama penyakit sesuai dengan urutan kelas model
# penyakit_classes = [
#     "acne", "carcinoma", "herpes", "milia", "nail fungus", "normal", "vitiligo"
# ]

# # Endpoint untuk memverifikasi token JWT dan melakukan prediksi
# @app.route('/predict', methods=['POST'])
# @jwt_required()  # Menambahkan decorator ini untuk memastikan hanya request yang sudah terverifikasi yang bisa >
# def predict():
#     # Mengambil data user dari token
#     current_user = get_jwt_identity()
#     print(f"User ID dari token: {current_user}")

#     if 'image' not in request.files:
#         return jsonify({'error': 'Upss, Kamu belum upload foto ya!'}), 400

#     file = request.files['image']
#     if file.filename == '':
#         return jsonify({'error': 'Upss, Kamu belum upload foto ya!'}), 400
#         # Membaca gambar dari file yang diupload
#     img = Image.open(io.BytesIO(file.read()))
#     img = img.resize((224, 224))  # Ukuran input model (224x224x3)
#     img_array = np.array(img) / 255.0  # Normalisasi nilai piksel gambar
#     img_array = np.expand_dims(img_array, axis=0)  # Menambahkan dimensi batch (1 gambar dalam batch)

#     # Persiapkan input tensor untuk model TFLite
#     input_details = interpreter.get_input_details()
#     output_details = interpreter.get_output_details()

#     # Persiapkan input tensor dan melakukan prediksi
#     input_data = np.array(img_array, dtype=np.float32)
#     interpreter.set_tensor(input_details[0]['index'], input_data)
#     interpreter.invoke()

#     # Menarik hasil output prediksi
#     output_data = interpreter.get_tensor(output_details[0]['index'])
#     prediction = output_data[0]
    
#     # Menentukan kelas penyakit berdasarkan hasil prediksi
#     predicted_class_index = np.argmax(prediction)  # Mengambil index kelas dengan probabilitas tertinggi
#     predicted_class = penyakit_classes[predicted_class_index]
#     confidence = prediction[predicted_class_index]  # Confidence dari model untuk prediksi ini

#     # Membuat pesan sesuai dengan hasil prediksi berdasarkan confidence
#     if predicted_class == "normal":
#         message = "Kulit terlihat normal dan sehat. Tidak terindikasi penyakit. Tetap jaga kesehatan kulitmu ya!"
#     elif confidence <= 0.4:
#         message = "Risiko terkena penyakit sangat kecil. Aman kok, stay safe ya!!!"
#     elif 0.4 < confidence <= 0.6:
#         message = f"Kemungkinan terkena penyakit {predicted_class} ada, tetapi masih belum terlalu signifikan."
#     else:  # confidence > 0.6
#         message = f"Ya, kamu terindikasi terkena penyakit {predicted_class} dengan tingkat keyakinan yang tinggi. Disarankan segera memeriksakan diri ke dokter."

#     # Kembalikan hasil prediksi dan pesan sebagai JSON
#     return jsonify({
#         'prediction': predicted_class,
#         'confidence': float(confidence),
#         'message': message
#     })

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8080)