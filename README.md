# AI-Driven Password Strength Checker & Security Dashboard

A full-stack cybersecurity application that uses Machine Learning to evaluate password strength more intelligently. Instead of only checking password length or character combinations with regular expressions (Regex), the system analyzes password patterns and common human behaviors to identify weak or predictable passwords, supported by a secure, cryptographically hashed backend database architecture.

## Key Architectural Features
* **Intelligent AI Pattern Classification:** A trained Scikit-learn machine learning model evaluates passwords based on real-world password patterns, common keyboard sequences, and predictable user habits. This provides a realistic assessment of password security than traditional password checkers.
* **Cryptographically Secure Architecture:** User information is protected using SHA-256 hashing combined with unique salts. Passwords are never stored in plain text, ensuring a secure authentication process.
* **FastAPI Backend:** The backend is built with FastAPI, providing a fast and efficient REST API. Rate limiting is implemented to help prevent brute-force attacks and excessive requests.
* **Interactive Security Dashboard:** A React-based dashboard displays password strength results, security statistics, and database insights through a modern and responsive user interface.

## Tech Stack & Ecosystem

**Frontend (Interactive Dashboard):** React.js, HTML, CSS
**Backend (High Performance API):** Python, FastAPI, Uvicorn
**Machine Learning:** Scikit-learn, Joblib
**Database (Data Storage):** SQLite
**Security:** SHA-256 Hashing with Salt

## Project Structure

```text
password_strength_checker/
├── ai_model/      # Machine learning models training scripts, feature engineering and serialized (.joblib) assets
├── backend/       # FastAPI backend, cryptographic utility tools and database schemas
├── data/          # Training datasets and resources
└── frontend/      # React.js web dashboard components, views and styling
```

## Local Development Setup
### Prerequisites
* Python 3.10+
* Node.js & npm
* Ubuntu Virtual Environment / Linux terminal

### 1. Backend & AI Engine Setup
Navigate to the backend directory, initialize a clean Python virtual environment, and install the verified dependencies.

#### From the root directory
cd backend 
python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 8000

### 2. Frontend Dashboard Setup
Open a new terminal window, navigate to the frontend directory, install the required packages and run:

cd frontend
npm install
npm start

## Educational Cybersecurity Disclaimer
This project was developed strictly for education and portfolio purposes to demonstrate the integration of machine learning, cybersecurity concepts, and full stack web developments. It is not intended for handling real-world sensitive credentials in a production environment.
