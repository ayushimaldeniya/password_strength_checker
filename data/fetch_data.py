import os    #to manage files
import urllib.request   #to talk to the internet

#configuration paths
DATASET_URL = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt"
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "raw_passwords.txt")

def dowload_dataset():
    #ensure the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        print(f"Creating output directory: {OUTPUT_DIR}")
        os.makedirs(OUTPUT_DIR)

    #download the dataset
    print(f"Downloading password dataset from SecLists...")
    try:
        #Open a connection to the dataset URL and download the file
        with urllib.request.urlopen(DATASET_URL) as response, open(OUTPUT_FILE, 'wb') as out_file:
            data = response.read()  # Read the content of the response
            out_file.write(data)    # Write the content to the output file
        print(f"Success! Dataset saved to: {OUTPUT_FILE}")
    
    except Exception as e:
        print(f"An error occured during download: {e}")

if __name__ == "__main__":
    dowload_dataset()
