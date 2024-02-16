import os
import socket

def send_video(host, port, file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Extract the file name and size
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # Send the file name and size to the server
    client_socket.sendall(f"{file_name},{file_size}".encode())

    # Send the file data in chunks
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            client_socket.sendall(chunk)

    print("[*] Video executable sent to the server")

    # Wait to receive the screen_record.avi file from the server
    receive_file(client_socket, "screen_record.avi")

    # Close the client socket
    client_socket.close()

def receive_file(client_socket, save_path):
    file_info = bytearray(client_socket.recv(1024))
    file_name, file_size = file_info.decode('utf-8').split(',')
    file_size = int(file_size)

    received_data = bytearray()
    while len(received_data) < file_size:
        chunk = client_socket.recv(min(4096, file_size - len(received_data)))
        if not chunk:
            break
        received_data += chunk

    with open(save_path, "wb") as f:
        f.write(received_data)

    print(f"[*] {file_name} received from the server")

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 12345
    FILE_PATH = "C:\\Users\\profe\\Desktop\\video\\client\\video.exe"
    send_video(HOST, PORT, FILE_PATH)
