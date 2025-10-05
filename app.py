# ExoForge/app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score
import os
import traceback 

app = Flask(__name__)

# --- Configuration and Model Loading ---
MODEL_PATH = 'saved_models/catboost_model.pkl'
SCALER_PATH = 'saved_models/scaler.pkl'
DATA_PATH = 'data/processed_combined.csv'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# This hard-coded list ensures the model always gets the data in the order it expects.
FEATURE_ORDER = [
    'period', 'duration', 'depth', 'planet_radius', 'equilibrium_temp', 
    'insolation_flux', 'model_snr', 'stellar_temp', 'stellar_logg', 'stellar_radius'
]

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("Initial model and scaler loaded successfully.")
except Exception as e:
    model, scaler = None, None
    print(f"CRITICAL WARNING: Could not load model or scaler. Prediction will fail. Error: {e}")

# --- Basic and Static Routes ---
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/')
def home():
    return render_template('index.html')

# --- DEFINITIVE, FIXED STATUS ROUTE ---
@app.route('/status', methods=['GET'])
def status():
    if not model or not scaler:
        return jsonify({'accuracy': 'N/A - Model not loaded'})
    try:
        df = pd.read_csv(DATA_PATH)
        # Ensure the columns used for splitting match the FEATURE_ORDER
        X = df[FEATURE_ORDER]
        y = df['disposition']
        
        # We calculate accuracy on a consistent test split of the data
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
        X_test_scaled = scaler.transform(X_test)
        
        accuracy = accuracy_score(y_test, model.predict(X_test_scaled))
        return jsonify({'accuracy': f"{accuracy:.2%}"})
    except Exception as e:
        print(f"Error in /status route: {e}")
        return jsonify({'accuracy': 'Error'}), 500

# --- PREDICT FUNCTION ---
@app.route('/predict', methods=['POST'])
def predict():
    if not model or not scaler:
        return jsonify({'error': 'Model or scaler not loaded on the server.'}), 500
    try:
        data = request.get_json()
        input_data = [float(data.get(feature, 0.0)) for feature in FEATURE_ORDER]
        input_df = pd.DataFrame([input_data], columns=FEATURE_ORDER)
        input_scaled = scaler.transform(input_df)
        
        prediction = int(model.predict(input_scaled)[0])
        probabilities = model.predict_proba(input_scaled)[0]
        
        confidence_dict = {
            'CONFIRMED': probabilities[2],
            'CANDIDATE': probabilities[1],
            'FALSE_POSITIVE': probabilities[0]
        }

        label_map = {2: "CONFIRMED EXOPLANET", 1: "CANDIDATE", 0: "FALSE POSITIVE"}
        result = {'prediction': label_map.get(prediction, "Unknown"), 'confidence': confidence_dict}
        return jsonify(result)

    except Exception as e:
        print("--- PREDICTION ERROR ---")
        print(traceback.format_exc())
        return jsonify({'error': 'An internal error occurred during prediction.'}), 500

# --- RETRAIN ROUTE (RESTORED) ---
@app.route('/retrain', methods=['POST'])
def retrain():
    global model, scaler
    try:
        params = request.get_json()
        df = pd.read_csv(DATA_PATH)
        X = df[FEATURE_ORDER]
        y = df['disposition']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
        
        # Re-initialize and fit the scaler on the new training data
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        new_model = CatBoostClassifier(
            iterations=int(params.get('iterations')),
            learning_rate=float(params.get('learning_rate')),
            depth=int(params.get('depth')),
            verbose=False
        )
        new_model.fit(X_train_scaled, y_train)
        accuracy = accuracy_score(y_test, new_model.predict(X_test_scaled))
        
        # Update the global model and save both the new model and scaler
        model = new_model
        joblib.dump(model, MODEL_PATH)
        joblib.dump(scaler, SCALER_PATH)
        
        return jsonify({'message': 'Retraining successful!', 'new_accuracy': f"{accuracy:.2%}"})
    except Exception as e:
        print(f"--- RETRAIN ERROR --- \n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

# --- SIMULATOR ROUTES ---
@app.route('/simulator')
def simulator():
    """Serves the Animation.html file from inside the 'galaxy' directory."""
    return send_from_directory('galaxy', 'Animation.html')

@app.route('/galaxy/<path:filename>')
def serve_galaxy_files(filename):
    """Serves texture files from the 'galaxy' directory for the simulator."""
    return send_from_directory('galaxy', filename)

if __name__ == '__main__':
    os.makedirs('saved_models', exist_ok=True)
    app.run(debug=True)