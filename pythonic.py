from flask import Flask, render_template, request, jsonify, url_for, redirect
import json
from werkzeug.utils import secure_filename
import os
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from tensorflow import keras
from tensorflow.keras.preprocessing import image

# Create Flask app instance
app = Flask(__name__)

# Configure app settings
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Load the model
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "models", "Bone-Fracture-Detection---MURA-master", "save_models", "MURA_modle@epochs50.h5"
)

model = None

try:
    if os.path.exists(MODEL_PATH):
        model = keras.models.load_model(MODEL_PATH, compile=False)
        print("Model loaded successfully!")
    else:
        print(f"Model not found at {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {str(e)}")

def predict_image(image_path):
    try:
        if model is None:
            return {"success": False, "error": "Model not loaded properly"}
        
        img = Image.open(image_path).convert('L')
        img = img.resize((320, 320))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        img_array = np.expand_dims(img_array, axis=-1)

        prediction = model.predict(img_array)
        confidence = float(prediction[0][0])  # أو prediction.squeeze() لو رجع array أكبر

        
        # تحديد التشخيص والتفاصيل
        if confidence > 0.5:
            severity = "Moderate" if confidence > .4 else "Mild"
            location = determine_fracture_location(confidence)
            diagnosis = {
                "primary_finding": f"Fracture detected in the {location}",
                "severity": severity,
                "confidence": f"{confidence * 100:.1f}%",
                "additional_observations": [
                    "Minor bone density reduction",
                    "No signs of arthritis",
                    "Normal joint spacing"
                ],
                "recommendations": [
                    "Immediate immobilization recommended",
                    "Schedule follow-up in 2 weeks",
                    "Consider physical therapy after healing"
                ]
            }
        else:
            diagnosis = {
                "primary_finding": "No fracture detected",
                "confidence": f"{(1-confidence) * 100:.1f}%",
                "additional_observations": [
                    "Normal bone density",
                    "No signs of arthritis",
                    "Normal joint spacing"
                ],
                "recommendations": [
                    "No immediate treatment needed",
                    "Regular check-up recommended"
                ]
            }
        
        return {
            "success": True,
            "prediction": confidence,
            "diagnosis": diagnosis
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def determine_fracture_location(confidence):
    # يمكن تحسين هذه الدالة بناءً على نموذج أكثر تفصيلاً
    locations = ["distal radius", "proximal humerus", "ulnar shaft", "wrist"]
    return locations[0]  # حالياً نعيد موقع ثابت، يمكن تحسينه لاحقاً

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/getStarted')
def getStarted():
    return render_template('getStarted.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/doc')
def doc():
    return render_template('doc.html')

@app.route('/reg')
def reg():
    return render_template('reg.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})

        # Save the uploaded file
        upload_folder = os.path.join(app.static_folder, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # Process image for model
        img = image.load_img(file_path, target_size=(320, 320), color_mode='grayscale')
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        # Make prediction
        prediction = model.predict(img_array)
        probability = float(prediction[0][0])
        print(probability)

        # Determine result
        result = "Fracture Detected" if probability < 0.5 else "No Fracture Detected"
        description = (
            "No significant bone fracture detected. Regular checkup recommended." 
            if probability > 0.5 
            else "A fracture has been detected in the uploaded X-ray image. Please ensure the affected area remains immobilized. Refer the patient to an orthopedic specialist for further evaluation. Pain management and advanced imaging (e.g., CT or MRI) may be considered if clinically indicated."
        )
        diagnosis = {
            'result': result,
            'description': description,
            'confidence': round(max(probability, 1-probability) * 100, 2)
        }

        return jsonify({
            'success': True,
            'file_path': f'/static/uploads/{file.filename}',
            'diagnosis': diagnosis
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/results')
def results():
    image_path = request.args.get('image')
    diagnosis_data = request.args.get('diagnosis')
    
    try:
        diagnosis = json.loads(diagnosis_data) if diagnosis_data else None
        return render_template('results.html', 
                             image_path=image_path,
                             diagnosis=diagnosis)
    except Exception as e:
        return redirect(url_for('home'))

# Add this route with your other routes
# Update your sign_in route
@app.route('/sign_in.html')  # Changed from '/sign_in'
def sign_in():
    return render_template('sign_in.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
