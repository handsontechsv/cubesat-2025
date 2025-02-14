import socket
import os
from picamera2 import Picamera2
from datetime import datetime

SERVER_HOST = "0.0.0.0" 
SERVER_PORT = 8076
IMG_OUTPUT_FOLDER = "./pi"
IMAGE_PREFIX = "pi_"
IMAGE_SUFFIX = ".jpg"
RESOLUTION = "800*600"

def generate_filename():
    now = datetime.now()
    date_time = now.strftime("%Y_%m_%d_%H:%M:%S")
    filename = IMAGE_PREFIX + date_time + IMAGE_SUFFIX
    return filename

def capture_image():
    filename = generate_filename()
    filepath = IMG_OUTPUT_FOLDER + '/' + filename

    resValues = RESOLUTION.split('*')
    
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (int(resValues[0]), int(resValues[1]))}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start()

    picam2.capture_file(filepath)
    picam2.stop()

    os.rename(filepath, './pi/test_image.jpg')
    return './pi/test_image.jpg'  

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

print(f"Listening on port {SERVER_PORT}...")

while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1500).decode()
    print(request)
    headers = request.split('\n')
    first_header_components = headers[0].split()

    http_method = first_header_components[0]
    path = first_header_components[1]
    
    if path == '/':
        with open('/home/pi/display.html') as fin:
            content = fin.read()
        response = 'HTTP/1.1 200 OK\n\n' + content
        client_socket.sendall(response.encode())
        client_socket.close()

    elif path == '/capture_photo':
        print("Taking a new picture...")
        # Take the picture and store it as 'test_image.jpg'
        capture_image()

        # Send a response that shows the picture
        response = (
            'HTTP/1.1 200 OK\n'
            'Content-Type: text/html\n\n'
            '<html><body><h1></h1>'
            '<img src="/test_image.jpg" alt="Captured Image">'
            '</body></html>'
        )

        # Send the response back to the client
        client_socket.sendall(response.encode())
        client_socket.close()

    elif path == '/test_image.jpg':
        with open('/home/pi/pi/test_image.jpg', 'rb') as file:
            image_data = file.read()

        response_headers = (
            'HTTP/1.1 200 OK\r\n'
            'Content-Type: image/jpeg\r\n'
            f'Content-Length: {len(image_data)}\r\n'
            'Connection: close\r\n'
            '\r\n'
        )
        
        client_socket.sendall(response_headers.encode('utf-8') + image_data)
        print('done sending')
        client_socket.close()
