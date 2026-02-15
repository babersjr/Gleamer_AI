from tensorflow.keras.models import load_model

try:
    model = load_model(r"models\fracture_classification_model.h5")
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading model:", e)
