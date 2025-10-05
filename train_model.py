import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from catboost import CatBoostClassifier
import lightgbm as lgb
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
import seaborn as sns
import matplotlib.pyplot as plt
import mlflow
import mlflow.catboost
import mlflow.sklearn
import mlflow.lightgbm

def train_exoplanet_model(processed_data_path, model_save_path, scaler_save_path):
    """
    Trains multiple classifiers, logs them, and saves the BEST ORIGINAL model
    (not the pyfunc wrapper) for the Flask app.
    """
    print("Starting multi-model training and MLflow experiment logging...")

    # --- 1. Data Preparation ---
    PERFORMANCE_DIR = 'model_performance'
    os.makedirs(PERFORMANCE_DIR, exist_ok=True)
    df = pd.read_csv(processed_data_path)
    X = df.drop('disposition', axis=1)
    y = df['disposition']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("Data preparation complete.")

    joblib.dump(scaler, scaler_save_path)
    print(f"Scaler saved locally to '{scaler_save_path}'")

    # --- 2. Define Models to Train ---
    models_to_train = {
        "CatBoost": {"model": CatBoostClassifier(iterations=1000, learning_rate=0.05, depth=8, verbose=0, early_stopping_rounds=50), "log_function": mlflow.catboost.log_model},
        "RandomForest": {"model": RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1), "log_function": mlflow.sklearn.log_model},
        "LightGBM": {"model": lgb.LGBMClassifier(n_estimators=1000, learning_rate=0.05, num_leaves=31, random_state=42, n_jobs=-1), "log_function": mlflow.lightgbm.log_model}
    }

    # --- 3. MLflow Experiment Tracking ---
    mlflow.set_experiment("ExoForge_Exoplanet_Classification")
    
    with mlflow.start_run(run_name="Model_Comparison_Parent_Run") as parent_run:
        print(f"\n--- MLflow Parent Run Started (ID: {parent_run.info.run_id}) ---")
        
        for model_name, config in models_to_train.items():
            with mlflow.start_run(run_name=f"Train_{model_name}", nested=True) as child_run:
                print(f"\n--- Training {model_name} (Run ID: {child_run.info.run_id}) ---")
                model = config["model"]
                log_model_func = config["log_function"]
                mlflow.log_param("model_class", model.__class__.__name__)
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                accuracy = accuracy_score(y_test, y_pred)
                mlflow.log_metric("accuracy", accuracy)
                print(f"  {model_name} Accuracy: {accuracy:.4f}")

                report_path = os.path.join(PERFORMANCE_DIR, f'{model_name}_report.txt')
                with open(report_path, 'w') as f: f.write(classification_report(y_test, y_pred, target_names=['False Positive', 'Candidate', 'Confirmed']))
                mlflow.log_artifact(report_path, "performance_reports")
                matrix_path = os.path.join(PERFORMANCE_DIR, f'{model_name}_confusion_matrix.png')
                plt.figure(figsize=(10, 7))
                sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
                plt.title(f'{model_name} Confusion Matrix')
                plt.savefig(matrix_path)
                plt.close()
                mlflow.log_artifact(matrix_path, "plots")
                log_model_func(model, artifact_path=model_name)
    
    print("\n--- All models trained. Identifying and saving the best model. ---")

    # --- 4. Find the Best Model ---
    client = mlflow.tracking.MlflowClient()
    child_runs = client.search_runs(experiment_ids=[parent_run.info.experiment_id], filter_string=f"tags.mlflow.parentRunId = '{parent_run.info.run_id}'")
    best_run = max(child_runs, key=lambda run: run.data.metrics["accuracy"])
    best_run_id = best_run.info.run_id
    best_model_name = best_run.data.params["model_class"]
    print(f"Best Model Found: {best_model_name} (Run ID: {best_run_id})")

    # --- 5. DEFINITIVE FIX: INTELLIGENTLY FIND AND SAVE THE ORIGINAL MODEL ---
    best_model_artifact_path = best_run.data.tags['mlflow.runName'].replace('Train_', '')
    local_path = mlflow.artifacts.download_artifacts(run_id=best_run_id, artifact_path=best_model_artifact_path)
    print(f"Downloaded best model artifacts to: {local_path}")
    
    # --- INTELLIGENT FILE FINDER ---
    # Search the downloaded directory for common model file names/extensions
    model_file_to_load = None
    possible_model_files = ["model.pkl", "model.cb", "model.txt"]
    for file_name in possible_model_files:
        potential_path = os.path.join(local_path, file_name)
        if os.path.exists(potential_path):
            model_file_to_load = potential_path
            print(f"Found model file to load: {model_file_to_load}")
            break
            
    if not model_file_to_load:
        raise FileNotFoundError(f"Could not find a valid model file in the downloaded artifacts at {local_path}")

    # Load the ORIGINAL model object from the found file
    if best_model_name == "CatBoostClassifier":
        # CatBoost needs a special loading method if it's not a pickle file
        original_model = CatBoostClassifier()
        original_model.load_model(model_file_to_load)
    else:
        original_model = joblib.load(model_file_to_load)
    
    joblib.dump(original_model, model_save_path)
    print(f"Best ORIGINAL model ({best_model_name}) saved to '{model_save_path}'. This will have '.predict_proba'.")

    # Register the model in MLflow registry
    model_uri = f"runs:/{best_run_id}/{best_model_artifact_path}"
    mlflow.register_model(model_uri, "ExoForge-Classifier")
    print("Model registered in MLflow successfully.")

if __name__ == '__main__':
    PROCESSED_DATA_PATH = 'data/processed_combined.csv'
    MODEL_SAVE_PATH = 'saved_models/catboost_model.pkl'
    SCALER_SAVE_PATH = 'saved_models/scaler.pkl'
    train_exoplanet_model(PROCESSED_DATA_PATH, MODEL_SAVE_PATH, SCALER_SAVE_PATH)