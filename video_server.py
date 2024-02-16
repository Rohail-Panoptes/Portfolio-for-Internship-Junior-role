import os
import socket
import subprocess  # Import the subprocess module

def receive_video(host, port, save_dir):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

        # Receive file name and size
        file_info = client_socket.recv(1024)
        file_name, file_size = file_info.split(b',')
        file_name = file_name.decode('utf-8')
        file_size = int(file_size)

        received_data = bytearray()
        while len(received_data) < file_size:
            chunk = client_socket.recv(min(4096, file_size - len(received_data)))
            if not chunk:
                break
            received_data += chunk

        file_path = os.path.join(save_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(received_data)

        print("[*] Video executable received at the server side")

        # Execute the video executable
        print("[*] Execution about to happen")
        try:
            subprocess.run([file_path], check=True)
            print("[*] Video executable executed successfully")
        except subprocess.CalledProcessError as e:
            print(f"[*] Error executing video executable: {e}")

        # Wait for screen_record.avi to be created
        while not os.path.exists("screen_record.avi"):
            pass

        print("[*] screen_record.avi file created")

        # Send screen_record.avi back to the client
        send_file(client_socket, "screen_record.avi")

        client_socket.close()

    server_socket.close()

def send_file(client_socket, file_path):
    # Get the size of the file
    file_size = os.path.getsize(file_path)

    # Send the file name and size to the client
    client_socket.sendall(f"{os.path.basename(file_path)},{file_size}".encode())

    # Send the file data in chunks
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            client_socket.sendall(chunk)

    print(f"[*] {file_path} sent successfully")

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 12345
    SAVE_DIR = "C:\\Users\\profe\\Desktop\\video\\server"
    receive_video(HOST, PORT, SAVE_DIR)
