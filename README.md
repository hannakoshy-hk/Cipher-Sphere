# Cipher Sphere

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-darkgreen)
![Cryptography](https://img.shields.io/badge/Cryptography-Enabled-critical)

Cipher Sphere is a Flask-based web application designed to demonstrate secure file and text encryption and decryption. The system ensures confidentiality by encrypting data locally before storage or sharing, making it suitable for cloud environments where security is a priority. Although developed and tested locally, the project represents a scalable model for secure encryption workflows in cloud-based systems.

## Features

- Encrypt and decrypt any type of file (text, images, videos, documents, etc.)
- A unique key is generated for every encryption, and the same key is required for decryption
- User login and authentication system
- Supports multiple strong cryptographic algorithms:
  - AES-CCM
  - AES-GCM
  - MultiFernet
  - ChaCha20-Poly
- Web interface developed using Flask, HTML, CSS, and Bootstrap
- Lightweight interface designed for accessible operation

---

## Tech Stack

| Component    | Technology                   |
| ------------ | ---------------------------- |
| Backend      | Python (Flask)               |
| Frontend     | HTML, CSS, Bootstrap         |
| Cryptography | Python `cryptography` module |
| Runtime      | Python                       |

## Install depedencied

pip install -r requirements.txt

## Start the Flask application

python app.py

## Screenshots

### Home Page

![Signup](screenshots/Signup.jpg)

### Encryption Page

![Login](screenshots/Login.jpg)

### Decryption Page

![Landing page](screenshots/Interface.jpg)
