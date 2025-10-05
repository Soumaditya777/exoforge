# ExoForge AI 🚀

### An End-to-End MLOps Platform for Exoplanet Classification

**Team:** House Stark  

---

## 📖 Introduction

ExoForge AI is a full-stack web application designed to accelerate the discovery of exoplanets. It addresses the significant challenge of analyzing the vast amounts of data from NASA's Kepler and TESS missions by providing an intelligent, interactive, and automated platform for classifying potential exoplanet signals.

The platform ingests real-world astronomical data, uses a powerful machine learning model to predict classifications, and presents the results in a user-friendly dashboard. It is all powered by a professional MLOps pipeline using MLflow, ensuring that the entire workflow is reproducible, versioned, and always powered by the best-performing model.

<!-- Add a GIF of your app in action here! -->
![ExoForge AI Demo](https-placeholder-for-your-demo-gif) 

## ✨ Key Features

-   **🤖 AI-Powered Analysis:** Instantly classifies exoplanet candidates into three categories: **Confirmed Exoplanet**, **Candidate**, or **False Positive** using a trained CatBoost model.
-   **📊 Interactive Dashboard:** A sleek, modern UI that provides a detailed analysis, including a classification verdict, confidence score, and a dynamic probability chart.
-   **🔬 'What-If' Scenarios:** Load real-world data presets and then freely edit the parameters to see how the AI's prediction changes in real-time.
-   **🪐 3D Solar System Simulator:** An interactive 3D visualization (built with Three.js) that displays planetary systems with data-driven tags, showing the classification status of each planet.
-   **🔧 On-the-Fly Model Calibration:** A configuration modal that allows users to adjust model hyperparameters and trigger a retraining cycle directly from the UI.
-   **🏭 Professional MLOps Pipeline:** An automated workflow that preprocesses data, trains multiple models (CatBoost, RandomForest, LightGBM), compares them using **MLflow**, and automatically saves the best-performing model for the application.

## 🛠️ Technology Stack

| Backend & MLOps             | Frontend                    |
| --------------------------- | --------------------------- |
| ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)         | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)             |
| ![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)           | ![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)               |
| ![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)           | ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black) |
| ![Scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikit-learn&logoColor=white) | **Three.js**                |
| **CatBoost / LightGBM**     | **Chart.js**                |
| **MLflow**                  | **Particles.js**            |

## 🏗️ Project Architecture: The MLOps Pipeline

The core of ExoForge AI is its automated "model factory." The workflow is designed for reproducibility and continuous improvement.

1.  **Orchestration (`run_pipeline.py`):** A master script that executes the entire pipeline with a single command.
2.  **Data Preprocessing (`preprocess_data.py`):** Ingests and cleans raw NASA data, creating a unified dataset.
3.  **Multi-Model Training (`train_model.py`):**
    -   Trains `CatBoost`, `RandomForest`, and `LightGBM` on the processed data.
    -   Uses **MLflow** to log all parameters, metrics, and visual artifacts (like confusion matrices) for each model in an organized, nested structure.
4.  **Best Model Selection:**
    -   The script programmatically queries MLflow to find the model with the highest accuracy.
    -   It downloads the artifacts for this winning model.
5.  **Model Saving:**
    -   The script saves the **original, fully-functional model object** (e.g., the raw CatBoost model with its `.predict_proba()` method) to the `saved_models/` directory.
    -   This ensures the Flask app always loads the best, most compatible model for predictions.

## ⚙️ Installation & Setup

Follow these steps to get the project running locally.

**Prerequisites:**
-   Python 3.9+
-   Git

**1. Clone the Repository**
```bash
git clone https://github.com/Soumaditya777/exoforge.git
cd exoforge
