import os
import string
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.hashing.hash_utils import generate_secure_salt, compute_salted_hash
from backend.database import get_db_connection, initialize_database
import sqlite3


# 1. Initialize the web application app instance
app = FastAPI(title="Predictive Password Defense API", version="1.0")

#Ensure database tables exists at launch
initialize_database()

# NEW: SECURITY CORS MIDDLEWARE CONFIGURATION
#Define the web origins permitted to stream network calls to our API
origins = [
    "http://localhost:3000",  # React frontend development server
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins to enhance security
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allows all custom request header options
)

# 2. Hardcode the absolute path globally so every function sees the exact same file
MODEL_PATH = "/home/IT24103820/password_strength_checker/ai_model/password_detector.joblib"
model = None

# Using a standard Pydantic schema to securely structure incoming requests
class PasswordCheckRequest(BaseModel):
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

@app.on_event("startup")
def load_assets():
    global model
    print("\nInitializing the Web Server and loading AI Model assets...")
    
    # 3. Clean, straightforward path verification (No 'not' inversion!)
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("AI Model loaded successfully into web server from disk.\n")
    else:
        print(f"Error: AI Model truly not found at {MODEL_PATH}.\n")
    
@app.get("/")
def home():
    return {"status": "online", "message": "Welcome to the Password Security Analysis Service Backend"}

@app.post("/api/analyze")
def analyze_password(request: PasswordCheckRequest):
    user_password = request.password

    if not user_password:
        return {"error": "Password input cannot be empty."}

    #LAYER 1: DETERMINISTIC RULE-BASED ENGINE
    #Real-time extraction of advanced math features
    pwd_len = len(user_password)
    has_lowercase = any(c.islower() for c in user_password)
    has_uppercase = any(c.isupper() for c in user_password)
    has_digits = any(c.isdigit() for c in user_password)
    has_symbols = any(c in string.punctuation for c in user_password)
    unique_ratio = len(set(user_password)) / pwd_len if pwd_len > 0 else 0

    #Calculate unique character ratio to catch simple repetitive loops (eg: "aaaaaaaa")
    rule_flags = []
    if pwd_len < 8:
        rule_flags.append("Password fails minimal length requirements (Must be 8+ characters).")
    if not (has_lowercase and has_uppercase):
        rule_flags.append("Missing case diversification (Mix uppercase and lowercase).")
    if not has_digits:
        rule_flags.append("Missing numercial complexity (Add digits 0-9).")
    if not has_symbols:
        rule_flags.append("Missing special character attributes.")
    if unique_ratio < 0.3:
        rule_flags.append("High structural redundancy detected (Avoid repetitive character loops).")

    is_rule_valid = len(rule_flags) == 0

    #LAYER 2: PREDICTIVE MACHINE LEARNING ENGINE
    pwd_digits = sum(1 for char in user_password if char.isdigit())
    character_variety = sum([has_lowercase, has_uppercase, has_digits, has_symbols])
    
    character_variety = 0
    if any(c.islower() for c in user_password): character_variety += 1
    if any(c.isupper() for c in user_password): character_variety += 1
    if any(c.isdigit() for c in user_password): character_variety += 1
    if any(c in string.punctuation for c in user_password): character_variety += 1

    feature_data = {
        'length': [pwd_len],
        'num_digits': [pwd_digits],
        'is_pure_numeric': [1 if user_password.isdigit() else 0],
        'digit_density': [pwd_digits / pwd_len if pwd_len > 0 else 0],
        'character_variety': [character_variety]
    }
    X_input = pd.DataFrame(feature_data)

    # Run prediction calculations if model exists
    if model is not None:
        prediction = int(model.predict(X_input)[0])
        probability = model.predict_proba(X_input)[0]
        ai_confidence = probability[1] if prediction == 1 else probability[0]
        ai_result = "vulnerable" if prediction == 1 else "secure"
    else:
        ai_result = "unknown"
        ai_confidence = 0.0

    #LAYER 3: CONSOLIDATED RISK THREAT VERDICT
    #If it  fails traditional rules or is predicted vulnerable by AI --> High Risk
    if not is_rule_valid or ai_result == "vulnerable":
        overall_risk = "HIGH RISK"
    elif ai_result == "secure" and ai_confidence > 0.85:
        overall_risk = "LOW RISK"
    else:
        overall_risk = "MEDIUM RISK"
  

    #LAYER 4: CRYPTOGRAPHIC HASHING FOR SECURE STORAGE
    secure_hash_data = None

    #Only spend processing cycles hashing if the password passes rules and isn't high risk
    if overall_risk == "LOW RISK":
        generated_salt = generate_secure_salt()
        crypto_hash = compute_salted_hash(user_password, generated_salt)
        secure_hash_data = {
            "salt_token": generated_salt,
            "generated_hash": crypto_hash,
            "hashing_algorithm": "SHA-256"
        }

    return {
        "summary": {
            "password_length": pwd_len,
            "overall_risk_assessment": overall_risk,
            "policy_compliant": is_rule_valid
        }, 
        "rule_analysis": {
            "passed_checks": is_rule_valid,
            "vulnerability_notes": rule_flags
        }, 
        "ai_analysis": {
            "pattern_verdict": ai_result,
            "confidence_score": round(ai_confidence * 100, 2)
        },
        "cryptographic_payload": secure_hash_data
    }    

@app.post("/api/register")
def register_user(request: RegisterRequest):
    username = request.username.strip().lower()
    user_password = request.password

    if not username or not user_password:
        return {"success": False, "message": "Username and password fields cannot be empty."}

    # LAYER 1 & 2: EVALUATE PASSWORD STRENGTH
    pwd_len = len(user_password)
    has_lowercase = any(c.islower() for c in user_password)
    has_uppercase = any(c.isupper() for c in user_password)
    has_digits = any(c.isdigit() for c in user_password)
    has_symbols = any(c in string.punctuation for c in user_password)
    
    unique_ratio = len(set(user_password)) / pwd_len if pwd_len > 0 else 0
    rule_flags = []
    if pwd_len < 8:
        rule_flags.append("Too short.")
    if not (has_lowercase and has_uppercase):
        rule_flags.append("Mix case colors.")
    
    is_rule_valid = len(rule_flags) == 0

    pwd_digits = sum(1 for char in user_password if char.isdigit())
    character_variety = sum([has_lowercase, has_uppercase, has_digits, has_symbols])
    
    X_input = pd.DataFrame({
        'length': [pwd_len], 'num_digits': [pwd_digits],
        'is_pure_numeric': [1 if user_password.isdigit() else 0],
        'digit_density': [pwd_digits / pwd_len if pwd_len > 0 else 0],
        'character_variety': [character_variety]
    })

    prediction = int(model.predict(X_input)[0]) if model is not None else 1
    ai_result = "vulnerable" if prediction == 1 else "secure"

    # Enforce policy block: If it's dangerous, do not let them register!
    if not is_rule_valid or ai_result == "vulnerable":
        return {
            "success": False, 
            "message": "Registration denied. Password pattern is too weak or predictable.",
            "flags": rule_flags
        }

    #LAYER 3: CRYPTOGRAPHIC GENERATION & WRITE
    generated_salt = generate_secure_salt()
    crypto_hash = compute_salted_hash(user_password, generated_salt)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Safe parameterized input query to block SQL injection attacks completely
        cursor.execute("""
            INSERT INTO users (username, salt_token, stored_hash, risk_tier)
            VALUES (?, ?, ?, ?)
        """, (username, generated_salt, crypto_hash, "LOW RISK"))
        
        conn.commit()
        conn.close()
        return {"success": True, "message": f"Account '{username}' registered securely!"}
        
    except sqlite3.IntegrityError:
        return {"success": False, "message": "Username is already taken."}