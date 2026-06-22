import os
import pandas as pd

#Define our paths
DATA_DIR = "data"
INPUT_FILE = os.path.join(DATA_DIR, "raw_passwords.txt")

def load_and_inspect_data():
    print("Loading leaked password dataset into Pandas...")

    #Check if the file exists before reading it
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} does not exist. Run fetch_data.py first..")
        return

    #Read the text file into a Pandas dataframe
    #use errors='opacity' or 'skip' to handle weird character safely
    df = pd.read_csv(INPUT_FILE, names=["password"], skip_blank_lines=True, on_bad_lines='skip', engine='c')

    print(f"Successfully loaded {len(df)} passwords for analysis.")
    print("\n First 5 entries in our AI training data:")
    print(df.head())

    print("\nRunning feature Engineering Engine...")

    #Feature 1: Password Length
    df['length'] = df['password'].str.len()

    # Feature 2: Number of digits inside the password
    df['num_digits'] = df['password'].str.count(r'\d')
    
    # Feature 3: Is it entirely made of numbers? (Convert True/False to 1/0 for the AI)
    df['is_pure_numeric'] = df['password'].str.isdigit().astype(int)

    print("\n Done! Updated AI Training Dataset Matrix:")
    print(df[['password', 'length', 'num_digits', 'is_pure_numeric']].head(10))

    print("\n Statistical Insights from Leaked Passwords:")
    print(f" -> Average Password Length: {df['length'].mean():.2f} characters")
    print(f" -> Average Digit Count: {df['num_digits'].mean():.2f} numbers")
    print(f" -> Percentage of purely numeric passwords: {(df['is_pure_numeric'].mean() * 100):.2f}%")

if __name__ == "__main__":
    load_and_inspect_data()