# Cloud Data Integrity with AES-256 Encryption

## Overview

This project implements data integrity for files stored in Amazon S3 using AES-256 encryption and SHA-256 hashing. The process ensures that data remains confidential and verifies its integrity upon retrieval. 

## Project Structure

- `app.py`: Handles file upload to S3 with encryption.
- `check.py`: Checks the integrity of the file stored in S3.
- `altering.py`: Alters a file and uploads it to S3 with encryption.

## Installation

Before running the project, ensure you have the following dependencies installed:

```bash
pip install boto3 pycryptodome
```

## Usage

1. **Upload a File**: Use `app.py` to encrypt and upload a file to S3.

    ```bash
    python app.py
    ```

2. **Check File Integrity**: Use `check.py` to verify the integrity of the uploaded file.

    ```bash
    python check.py
    ```

3. **Alter and Re-upload a File**: Use `altering.py` to download, modify, and re-upload the file.

    ```bash
    python altering.py
    ```

## AES Key

The AES key used for encryption is generated dynamically and printed to the console during upload. Make sure to securely store this key as it is required for decrypting files.

## License

This project is licensed under the MIT License.
