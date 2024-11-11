import socket
import re
from webpage import web_page
from openweathermapapi import PrintWeatherInformation

city = 'London'

def WebServer():
    # Set up and open a socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        
        # Socket receive()
        request = conn.recv(1024)
        #print('Request:', request)
        request = request.decode()
        # Handle different paths
        if '/weather' in request:  # AJAX request for weather data
            match = re.search(r'city:(\w+)', request)
            if match:
                city = match.group(1)
                print(city)
            response = PrintWeatherInformation(city)  # Get the updated weather data
            print(response)
        else:  # Serve the main HTML page
            response = web_page()
            
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        
        # Socket close()
        conn.close()
