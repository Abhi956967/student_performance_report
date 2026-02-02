📊 End-to-End Student Performance Prediction — AWS Deployment

This repository contains a production-grade Machine Learning pipeline to predict student academic performance using demographic, socio-economic, and educational factors.

The project follows MLOps best practices including:
Modular pipeline design
Data ingestion & validation
Feature engineering
Model training & evaluation
Artifact tracking
Flask web app for inference
AWS Elastic Beanstalk deployment

🚀 Project Highlights

End-to-End ML pipeline
Automated training workflow
Model evaluation & versioning
REST API using Flask
Cloud deployment on AWS Elastic Beanstalk
Environment-based configuration
Scalable production setup

🧠 Problem Statement

Educational institutions want to predict student performance to:
Identify at-risk students early
Improve intervention strategies
Support academic planning
This system predicts a student’s final score based on input attributes.

🏗️ Architecture

Data Source
     ↓
Data Ingestion
     ↓
Data Validation
     ↓
Data Transformation
     ↓
Model Training
     ↓
Model Evaluation
     ↓
Model Registry
     ↓
Flask API
     ↓
AWS Elastic Beanstalk

🛠️ Tech Stack

Programming Language: Python
ML: Scikit-learn, Pandas, NumPy
Visualization: Matplotlib, Seaborn
Backend: Flask
Deployment: AWS Elastic Beanstalk
Experiment Tracking: MLflow (optional)
Version Control: Git & GitHub

📂 Project Structure

student_performance_report/
│
├── artifacts/
├── logs/
├── src/
│   ├── components/
│   ├── pipeline/
│   ├── entity/
│   ├── config/
│   ├── utils/
│   └── exception/
│
├── app.py
├── requirements.txt
├── setup.py
├── Dockerfile (optional)
├── .ebextensions/
├── templates/
├── static/
├── config.yaml
├── params.yaml
└── README.md

⚙️ Installation & Local Setup
1️⃣ Clone Repository

git clone https://github.com/your-username/student-performance-mlops.git
cd student-performance-mlops

2️⃣ Create Virtual Environment

python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

▶️ Run Training Pipeline

python src/pipeline/training_pipeline.py

🌐 Run Flask App Locally

python app.py
http://127.0.0.1:5000

☁️ Deploy to AWS Elastic Beanstalk

🔐 Prerequisites

AWS Account
AWS CLI configured
Elastic Beanstalk CLI installed

pip install awsebcli

🌱 Environment Variables (AWS Console)

Set these inside Elastic Beanstalk:

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
MONGO_URI= (if used)
MODEL_BUCKET= (if S3 used)

🔄 CI/CD (Optional)

You can integrate:
GitHub Actions
AWS CodePipeline
Docker + ECR
Workflow:

GitHub Push → Build → Test → EB Deploy

🛣️ Future Enhancements

MLflow Tracking
S3 Model Registry
Dockerized deployment
CI/CD pipeline
Monitoring with CloudWatch
Drift Detection
Streamlit Frontend
API authentication

👨‍💻 Author

Abhishek Maurya
Aspiring Data Scientist | MLOps Engineer
