import io
import shutil
from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from config import *
from keys import Key
from utils import *

app = Flask(__name__)

# Directories for uploads and keys
UPLOAD_FOLDER = 'uploads'
KEYS_FOLDER = 'keys'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['KEYS_FOLDER'] = KEYS_FOLDER

# Function to generate a key and save it to keys/key.pem
def generate_key():
    # Logic to generate the key (example: using cryptography library)
    # Replace this with your actual key generation code
    key_data = b'example_key_data'
    with open(os.path.join(app.config['KEYS_FOLDER'], 'key.pem'), 'wb') as key_file:
        key_file.write(key_data)

@app.route('/')
def index():
    files = os.listdir(ENCRYPTED_FOLDER)
    keys = os.listdir(KEYS_FOLDER)
    if(os.path.exists(UPLOAD_FOLDER)):
        shutil.rmtree(UPLOAD_FOLDER)
    return render_template('index.html',uploaded_files=files,keys_list=keys)

@app.route('/wrongkey')
def wrongkey():
    return render_template('wrongkey.html')

@app.route('/upload_key',methods=['POST'])
def upload_key():
    key_file = request.files['key_file']
    if(not key_file.filename.endswith(KEY_EXTENSION)):
        return render_template('invalidkey.html')
    key_file.save(os.path.join(app.config['KEYS_FOLDER'],key_file.filename))
    return redirect(url_for('index'))

@app.route('/gen_key',methods=['POST'])
def generate_key():
    k = Key()
    k.generateKeys()
    return send_file(
        io.BytesIO(k.getKeyAsByteString()),
        as_attachment=True,
        download_name='key.pem',
        mimetype='text/plain'
    )

@app.route('/upload', methods=['POST'])
def upload():
    # Check if "use_existing_key" option is selected
    use_existing_key = request.form.get('use_existing_key') == 'true'

    if use_existing_key:
        # Upload key
        existing_key = request.form.get('key_existing')
        k = Key()
        k.readFromDisk(existing_key,KEYS_FOLDER)
        file = request.files['file']
        targetFileName = os.path.join(file.filename)
        file.save(targetFileName)

        splitAndEncrypt(targetFileName,ENCRYPTED_FOLDER,k)
        deleteFile(targetFileName)

        return redirect(url_for('index'))
    else:
        # Generate key and download
        k = Key()
        k.generateKeys()
        file = request.files['file']
        targetFileName = os.path.join(file.filename)
        file.save(targetFileName)

        splitAndEncrypt(targetFileName,ENCRYPTED_FOLDER,k)
        deleteFile(targetFileName)


        return send_file(
            io.BytesIO(k.getKeyAsByteString()),
            as_attachment=True,
            download_name='key.pem',
            mimetype='text/plain'
        )

@app.route('/delete_key/<key>',methods=['GET'])
def delete_key(key):
    deleteFile(os.path.join(KEYS_FOLDER,key))
    return redirect(url_for('index'))

@app.route('/delete_file/<file>',methods=['GET'])
def delete_file(file):
    shutil.rmtree(os.path.join(ENCRYPTED_FOLDER,file))
    return redirect(url_for('index'))



@app.route('/download_file', methods=['POST'])
def download_file():
    filename = request.form.get('file')
    key = request.form.get('key')
    k = Key()
    k.readFromDisk(key,KEYS_FOLDER)
    try:
        splitAndDecrypt(filename,ENCRYPTED_FOLDER,k,UPLOAD_FOLDER)
        return send_file(os.path.join(UPLOAD_FOLDER,filename))
    except:
        return redirect(url_for('wrongkey'))

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('user.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'

    return render_template('login.html', mesage = mesage)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
