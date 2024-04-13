from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

# Fungsi untuk membuat kunci dari password
def generate_key(password, salt):
    password = password.encode('utf-8')
    salt = salt.encode('utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Panjang kunci dalam byte (256 bit)
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password)

# Fungsi untuk enkripsi teks
def encrypt(plaintext, password , salt):
    key = generate_key(password,salt)
    plaintext = plaintext.encode('utf-8')
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    iv = b'1234567890123456'  # Inisialisasi vektor inisialisasi
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(ciphertext).decode()

# Fungsi untuk dekripsi teks
def decrypt(ciphertext_string, password , salt):
    key = generate_key(password,salt)
    ciphertext = base64.b64decode(ciphertext_string)
    iv = b'1234567890123456'  # Inisialisasi vektor inisialisasi
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data.decode()

# teksTerenkripsi = encrypt("Root2107#","Sanglah","250324")
# print("Teks Terenkripsi :", teksTerenkripsi)


# teksTerdeskripsi = decrypt("ukTE6EXmVHi3zLVq97mScA==", "Kembar" , "250324")
# print("Teks Terdeskripsi :", teksTerdeskripsi)

# def olahInputan(text, pas, s):
#     plaintext =text.encode('utf-8')
#     password = pas.encode('utf-8')
#     salt = s.encode('utf-8')
#     print("Teks Asli : ", text )
#     return plaintext , password , salt
#
#
#
# plaintext , password , salt = olahInputan("Denpasar", "Teknisi" , "250324")
#
# # # Teks yang akan dienkripsi
# # text = "Denpasar"
# # print("Teks : ", text)
# # plaintext = text.encode('utf-8')
# # #plaintext = b"{text}"
# #
# # # Kunci yang digunakan untuk enkripsi/dekripsi
# # password_string = "IPutuKembar"
# # salt_string = "250324"
# # password = password_string.encode('utf-8')
# # salt = salt_string.encode('utf-8')
#
# # Membuat kunci dari password
# key = generate_key(password, salt)
#
# # Enkripsi teks
# ciphertext = encrypt(plaintext, key)
# #print(ciphertext)
# enkripsi_string = base64.b64encode(ciphertext).decode()
# print("Teks Terenkripsi:", enkripsi_string)
#
# # Dekripsi teks
# decrypted_text = decrypt(ciphertext, key)
# #print("Teks Terdekripsi:", decrypted_text.decode())
#
#
# #coba dekripsi
# text_terinkripsi = base64.b64decode(enkripsi_string)
# decrypted_text = decrypt(text_terinkripsi, key)
# print("Teks Terdekripsi:", decrypted_text.decode())