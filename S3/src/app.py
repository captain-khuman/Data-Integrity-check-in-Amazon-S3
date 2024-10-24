import boto3
import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def generate_aes_key():
    """Generate a random 32-byte (256-bit) AES key."""
    return os.urandom(32)

def encrypt_file(file_data, key):
    """
    Encrypt the file data using AES encryption in CBC mode.
    
    Parameters:
        file_data (bytes): The raw data of the file to be encrypted.
        key (bytes): The AES key used for encryption.
    
    Returns:
        bytes: The initialization vector (IV) concatenated with the encrypted data.
    """
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))
    return iv + encrypted_data

def upload_file_with_hash(file_name, bucket_name, file_key):
    """
    Upload a file to S3 after encrypting it and generating a hash.
    
    Parameters:
        file_name (str): The name of the file to be uploaded.
        bucket_name (str): The S3 bucket where the file will be stored.
        file_key (str): The key under which the file will be stored in S3.
    """
    s3 = boto3.client('s3')
    key = generate_aes_key()
    print(f"Generated AES Key: {key.hex()}")

    try:
        with open(file_name, 'rb') as file:
            file_data = file.read()

        encrypted_data = encrypt_file(file_data, key)
        file_hash = hashlib.sha256(file_data).hexdigest()

        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=encrypted_data,
            Metadata={'filehash': file_hash}
        )
        print(f"File uploaded successfully with hash: {file_hash}")

    except Exception as e:
        print(f"Error uploading file: {str(e)}")

if __name__ == "__main__":
    file_name = 'test_file.txt'
    bucket_name = 'minor-testing-bucket'
    file_key = 'test_file.txt'
    upload_file_with_hash(file_name, bucket_name, file_key)
