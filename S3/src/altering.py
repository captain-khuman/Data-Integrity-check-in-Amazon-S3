import boto3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

# Initialize the S3 client
s3 = boto3.client('s3')

# Define the S3 bucket and file details
bucket_name = 'minor-testing-bucket'  # S3 bucket name
file_key = 'test_file.txt'  # Key for the file in S3
local_file = 'test_file.txt'  # Local filename to store the downloaded file

# Replace with your actual AES key
key = bytes.fromhex('replace-with-aes-key')  # Use the key printed by app.py

def encrypt_file(file_path, key):
    """
    Encrypt the file data using AES encryption in CBC mode.
    
    Parameters:
        file_path (str): The path to the file to encrypt.
        key (bytes): The AES key used for encryption.
    
    Returns:
        bytes: The encrypted file data, including the IV.
    """
    # Generate a random initialization vector (IV)
    iv = os.urandom(AES.block_size)  # Create a random IV
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Create AES cipher with the IV

    # Read the original file data
    with open(file_path, 'rb') as f:
        file_data = f.read()  # Read the entire file

    # Encrypt the file data and prepend the IV
    encrypted_data = iv + cipher.encrypt(pad(file_data, AES.block_size))
    return encrypted_data

# Step 1: Download the original file from S3
s3.download_file(bucket_name, file_key, local_file)  # Download the file to local storage

# Step 2: Alter the file (for example, append a string)
with open(local_file, 'a') as f:
    f.write('\nThis is altered content.')  # Append new content to the file

# Step 3: Encrypt the altered file before uploading
encrypted_data = encrypt_file(local_file, key)  # Encrypt the altered file data

# Step 4: Get the existing metadata
response = s3.head_object(Bucket=bucket_name, Key=file_key)  # Retrieve metadata for the existing file
existing_metadata = response['Metadata']  # Extract the existing metadata

# Step 5: Upload the encrypted altered file with the original metadata
s3.put_object(Bucket=bucket_name, Key=file_key, Body=encrypted_data, Metadata=existing_metadata)  # Upload the file

print("File altered, encrypted, and uploaded. Integrity check will fail.")  # Notify that the process is complete
