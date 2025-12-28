A simple file encryption desktop application built for study and experimentation. It allows users to encrypt and decrypt files using AES-GCM encryption with secure key derivation through the Scrypt algorithm.

<img width="1408" height="597" alt="frame" src="https://github.com/user-attachments/assets/b34293bd-f04b-421c-81a7-b5eee275bd94" />

## Cryptography

### Algorithms

* **Encryption**: AES-256
* **Mode**: GCM (Galois/Counter Mode)
* **Key Derivation**: Scrypt

### Process

1. **Key Derivation**

   * A key is derived from the user password using Scrypt
   * Parameters: `N=16384`, `r=8`, `p=1`
   * A random 32-byte salt is generated per operation

2. **Encryption (AES-GCM)**

   * A random 16-byte nonce is generated
   * The file is encrypted using AES-256-GCM
   * GCM provides confidentiality and integrity via a 16-byte authentication tag

3. **Encrypted File Format**

   ```
   [32 bytes Salt][16 bytes Nonce][Encrypted Data][16 bytes Auth Tag]
   ```

4. **Decryption**

   * Salt and nonce are read from the encrypted file
   * The key is derived again from the password and salt
   * The authentication tag is verified before decryption

## Tech Stack

* **Python 3**
* **Flet**
* **PyCryptodome**

## Usage

### Install

```bash
git clone https://github.com/devIasminSilva/secret-keeper.git
cd secret-keeper
pip install -r requirements.txt
```

### Run

```bash
python run.py
```

https://github.com/user-attachments/assets/db858705-b4ce-4a99-b229-ca72dca2155f




