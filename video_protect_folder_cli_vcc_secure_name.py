import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import argparse
import getpass
import struct

custom_ext = ".vcc"

def pad(data):
    return data + b"\0" * (16 - len(data) % 16)

def unpad(data):
    return data.rstrip(b"\0")

def encrypt_name(name, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_name = pad(name.encode("utf-8"))
    return cipher.encrypt(padded_name)

def decrypt_name(encrypted_name, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(encrypted_name)
    return unpad(decrypted).decode("utf-8")

def process_file(file_path, key, output_path, mode):
    key32 = key.encode("utf-8").ljust(32, b'\0')[:32]

    if mode == "encrypt":
        iv = get_random_bytes(16)
        cipher = AES.new(key32, AES.MODE_CBC, iv)

        with open(file_path, "rb") as f:
            plaintext = pad(f.read())

        encrypted = cipher.encrypt(plaintext)

        original_name = os.path.basename(file_path)
        encrypted_name = encrypt_name(original_name, key32)
        name_length = len(encrypted_name)

        with open(output_path, "wb") as f:
            f.write(iv)
            f.write(struct.pack("H", name_length))
            f.write(encrypted_name)
            f.write(encrypted)

    elif mode == "decrypt":
        with open(file_path, "rb") as f:
            iv = f.read(16)
            name_length = struct.unpack("H", f.read(2))[0]
            encrypted_name = f.read(name_length)
            ciphertext = f.read()

        original_name = decrypt_name(encrypted_name, key32)
        cipher = AES.new(key32, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext))

        with open(output_path, "wb") as f:
            f.write(plaintext)

        return original_name

def process_folder(input_dir, output_dir, key, mode):
    counter = 1
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            full_input_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_input_path, input_dir)

            if mode == "encrypt":
                fake_name = f"{counter:05d}{custom_ext}"
                output_file = os.path.join(output_dir, fake_name)
                counter += 1
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                print(f"🔐 Mã hóa: {rel_path} -> {fake_name}")
                process_file(full_input_path, key, output_file, mode)

            elif mode == "decrypt":
                if not file.endswith(custom_ext):
                    continue
                temp_output = os.path.join(output_dir, "temp_output")
                os.makedirs(os.path.dirname(temp_output), exist_ok=True)
                original_name = process_file(full_input_path, key, temp_output, mode)

                real_output_path = os.path.join(output_dir, original_name)
                os.replace(temp_output, real_output_path)
                print(f"🔓 Giải mã: {file} -> {original_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🔐 Mã hóa / Giải mã thư mục ẩn tên bằng AES")
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="encrypt hoặc decrypt")
    parser.add_argument("input_dir", help="Thư mục đầu vào")
    parser.add_argument("output_dir", help="Thư mục đầu ra chứa kết quả")

    args = parser.parse_args()
    password = getpass.getpass("🔑 Nhập mật khẩu: ")

    process_folder(args.input_dir, args.output_dir, password, args.mode)
