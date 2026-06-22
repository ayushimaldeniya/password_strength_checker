import os
import random
import string
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

#Path to the data we engineered in analyze_data.py
DATA_PATH = os.path.join("data", "raw_passwords.txt")

def generate_strong_password():
    # Make the length range overlap with the weak dataset (8 to 16 characters)
    # This forces the AI to look at character complexity, not just length!
    length = random.randint(8, 16)
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def build_and_train_ai():
    print("Reloading engineered data matrix...")

    #1. Load the week passwords (label = 1)
    # Define our target label: 1 means 'vulnerable/weak'
    # Since these are all leaked passwords, they are all marked 1
    df_weak = pd.read_csv(DATA_PATH, header=None, names=["password"], skip_blank_lines=True, on_bad_lines='skip', engine='c', dtype={"password": str})
    df_weak = df_weak.dropna()
    
    #HUMAN DATA INJECTION START
    #Manually inject long but incredibly weak passwords to mimic human laziness
    lazy_long_passwords = [
        "supercomputer123", "password123456789", "administrator2026", 
        "iloveyouforyears", "letmeinsecret123", "welcome2026!!!!",
        "qwertyuiopasdfgh", "monkey123456789", "shadowhunter12"
    ] * 100  # Duplicate them to make sure the AI takes them seriously

    df_lazy = pd.DataFrame({"password": lazy_long_passwords})
    df_weak = pd.concat([df_weak, df_lazy], ignore_index=True)
    df_weak['is_vulnerable'] = 1
    # HUMAN DATA INJECTION END

    #2. Generate an equal amount of strong passwords (label = 0)
    print("Generating secure negative samples to balance the dataset...")
    num_samples = len(df_weak)
    strong_passwords = [generate_strong_password() for _ in range(num_samples)]

    df_strong = pd.DataFrame({"password": strong_passwords})
    df_strong['is_vulnerable'] = 0

    #3. Combine the weak and strong datasets
    df = pd.concat([df_weak, df_strong], ignore_index=True)

    #4. Run Feature Engineering on the entire combined dataset
    df['length'] = df['password'].str.len()
    df['num_digits'] = df['password'].str.count(r'\d')
    df['is_pure_numeric'] = df['password'].str.isdigit().astype(int)

    #new feature 1: a digit density ratio (number of digits / total length) to capture how "digit-heavy" a password is
    df['digit_density'] = df['num_digits'] / df['length']

    #new feature 2: character variety score (1 to 4)
    def calculate_variety(pwd):
        score = 0
        if any(c.islower() for c in pwd): score += 1
        if any(c.isupper() for c in pwd): score += 1
        if any(c.isdigit() for c in pwd): score += 1
        if any(c in string.punctuation for c in pwd): score += 1
        return score
    
    df['character_variety'] = df['password'].apply(calculate_variety)

    #5. Split the data into features (x) and target (y)
    X = df[['length', 'num_digits', 'is_pure_numeric', 'digit_density', 'character_variety']]
    y = df['is_vulnerable']

    #6. Split into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Complete Dataset Size: {len(df)} rows")
    print(f"Training Split: {len(X_train)} rows | Testing Split: {len(X_test)} rows")
    
    #7. Initialize and train a simple Logistic Regression model
    print("\nTraining Predictive Logistic Regression Model...")
    model = LogisticRegression()
    model.fit(X_train, y_train)
    print("Training completed!")

    #8. Evaluate the model on the test set
    predictions = model.predict(X_test)
    print("\n AI Model Performace Evaluation Report:")
    print(classification_report(y_test, predictions))

    #9. Save the trained model
    MODEL_DIR = "ai_model"
    MODEL_FILE = os.path.join(MODEL_DIR, "password_detector.joblib")

    print("\nExporting trained AI model weights to disk...")
    joblib.dump(model, MODEL_FILE)
    print("Model saved successfully at:", MODEL_FILE)

if __name__ == "__main__":
    build_and_train_ai()
