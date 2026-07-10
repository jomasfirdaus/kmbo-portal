import base64
import hashlib
from django.contrib.auth.models import User, Group

import qrcode
from io import BytesIO

# Encrypt ID
def encrypt_id(id_encrypt):
    id_bytes = str(id_encrypt).encode('utf-8')
    encrypted_id = base64.b64encode(id_bytes).decode('utf-8')
    
    # Create a hash of the encrypted ID
    hash_object = hashlib.sha256(encrypted_id.encode('utf-8'))
    hashed_id = hash_object.hexdigest()
    
    return f"{hashed_id}-{encrypted_id}"

# Decrypt ID
def decrypt_id(encrypted_id):
    try:
        # Split the hash and the encrypted ID
        hashed_id, encrypted_id = encrypted_id.split('-', 1)
        
        # Verify the hash
        hash_object = hashlib.sha256(encrypted_id.encode('utf-8'))
        if hash_object.hexdigest() == hashed_id:
            decoded_id = base64.b64decode(encrypted_id.encode('utf-8')).decode('utf-8')
            return decoded_id
        else:
            return "Invalid ID"
    except Exception as e:
        # Handle decryption errors
        return "Invalid ID"

# Buka ID Foun
def getnewid(tabela):
    result = tabela.objects.last()
    id_foun = 1
    if result:
        id_foun += result.id

    return id_foun


# main/utils.py

def generate_qr_code_base64(url):
    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"