import boto3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

s3 = boto3.client('s3')

bucket_name = 'minor-testing-bucket'
file_key = 'test_file.txt'
local_file = 'test_file.txt'

key = bytes.fromhex('replace-with-aes-key')

def encrypt_file(file_path, key):
    """
    Encrypt the file data using AES encryption in CBC mode.
    
    Parameters:
        file_path (str): The path to the file to encrypt.
        key (bytes): The AES key used for encryption.
    
    Returns:
        bytes: The encrypted file data, including the IV.
    """
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(file_path, 'rb') as f:
        file_data = f.read()

    encrypted_data = iv + cipher.encrypt(pad(file_data, AES.block_size))
    return encrypted_data

s3.download_file(bucket_name, file_key, local_file)

with open(local_file, 'a') as f:
    f.write('\nThis is altered content.')

encrypted_data = encrypt_file(local_file, key)

response = s3.head_object(Bucket=bucket_name, Key=file_key)
existing_metadata = response['Metadata']

s3.put_object(Bucket=bucket_name, Key=file_key, Body=encrypted_data, Metadata=existing_metadata)

print("File altered, encrypted, and uploaded. Integrity check will fail.")
