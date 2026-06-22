import os
import joblib
import pandas as pd

MODEL_FILE = os.path.join("ai_model", "password_detector.joblib")

def interactive_test():
    # 1. Load the persistent model asset from the disk
    if not os.path.exists(MODEL_FILE):
        print(f"Error: Saved model not found at {MODEL_FILE}. Run train_model.py first.")
        return
        
    print("Waking up the Predictive AI Model...")
    model = joblib.load(MODEL_FILE)
    print("AI Engine Online! (Type 'exit' to quit)\n")
    
    while True:
        # 2. Capture a password input from the terminal
        user_password = input("Enter a password to test: ")
        if user_password.lower() == 'exit':
            print("Shutting down AI Engine. Goodbye!")
            break
            
        if not user_password:
            continue

        # 3. Transform the raw string into a real-time Feature DataFrame matching our training layout
        pwd_len = len(user_password)
        pwd_digits = sum(1 for char in user_password if char.isdigit())

        #Calculate character variety score matching the training matrix
        variety_score = 0
        if any(c.islower() for c in user_password): variety_score += 1
        if any(c.isupper() for c in user_password): variety_score += 1
        if any(c.isdigit() for c in user_password): variety_score += 1
        if any(c in r"!\#$%&'()*+,-./:;<=>?@[\]^_`{|}~" for c in user_password): variety_score += 1
        
        feature_data = {
            'length': [pwd_len],
            'num_digits': [pwd_digits],
            'is_pure_numeric': [1 if user_password.isdigit() else 0],
            'digit_density': [pwd_digits / pwd_len if pwd_len > 0 else 0],
            'character_variety': [variety_score]
        }
        X_input = pd.DataFrame(feature_data)
        
        # 4. Generate the prediction and statistical probability
        prediction = model.predict(X_input)[0]
        probability = model.predict_proba(X_input)[0]  # Returns [Prob(Safe), Prob(Vulnerable)]
        
        # 5. Display the Threat Intelligence Report
        print("-" * 50)
        if prediction == 1:
            print(f"RESULT: VULNERABLE/WEAK (Confidence: {probability[1]*100:.1f}%)")
            print(" -> Reason: This strongly mirrors common human patterns found in leaks.")
        else:
            print(f"RESULT: SECURE/STRONG (Confidence: {probability[0]*100:.1f}%)")
            print(" -> Reason: High complexity or randomized layout detected.")
        print("-" * 50 + "\n")

if __name__ == "__main__":
    interactive_test()