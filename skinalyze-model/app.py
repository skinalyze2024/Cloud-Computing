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
