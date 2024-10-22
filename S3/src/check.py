import boto3
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_file(encrypted_data, key):
    """
    Decrypt the encrypted file data using AES decryption in CBC mode.
    
    Parameters:
        encrypted_data (bytes): The encrypted file data including the IV.
        key (bytes): The AES key used for decryption.
    
    Returns:
        bytes: The decrypted file data.
    """
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)
    return decrypted_data

def check_file_integrity(bucket_name, file_key, key):
    """
    Check the integrity of a file stored in S3 by comparing the calculated hash 
    of the decrypted data with the stored hash in metadata.
    
    Parameters:
        bucket_name (str): The name of the S3 bucket.
        file_key (str): The key of the file in S3.
        key (bytes): The AES key used for decryption.
    """
    s3 = boto3.client('s3')

    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        encrypted_data = response['Body'].read()

        stored_hash = response['Metadata'].get('filehash', None)
        if not stored_hash:
            print(f"Error: 'filehash' not found in the metadata for {file_key}.")
            return

        decrypted_data = decrypt_file(encrypted_data, key)
        recalculated_hash = hashlib.sha256(decrypted_data).hexdigest()

        if recalculated_hash == stored_hash:
            print(f"File integrity check passed: {file_key}")
        else:
            print(f"File integrity check failed: {file_key}")

    except Exception as e:
        print(f"Error checking file integrity: {str(e)}")


if __name__ == "__main__":
    bucket_name = 'minor-testing-bucket'
    file_key = 'test_file.txt'
    key = bytes.fromhex('replace-with-aes-key')
    check_file_integrity(bucket_name, file_key, key)
