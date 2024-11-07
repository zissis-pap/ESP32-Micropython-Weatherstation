import socket

# Initialize a variable
counter = 0

# Function to return the counter value as plain text
def get_counter():
    global counter
    counter += 1  # Increment the counter
    return str(counter)

# Function for creating the
# web page to be displayed
def web_page():
    html_page = """
<html>
<head>
<meta name='viewport' content='width=device-width, initial-scale=1.0'/>
<script>
	var ajaxRequest = new XMLHttpRequest();
	function ajaxLoad(ajaxURL)
	{
		ajaxRequest.open('GET',ajaxURL,true);
		ajaxRequest.onreadystatechange = function()
		{
			if(ajaxRequest.readyState == 4 && ajaxRequest.status==200)
			{
				var ajaxResult = ajaxRequest.responseText;
				var tmpArray = ajaxResult.split("|");
				document.getElementById('temp').innerHTML = tmpArray[0];
				document.getElementById('humi').innerHTML = tmpArray[1];
			}
		}
		ajaxRequest.send();
	}
	function updateDHT()
	{
		ajaxLoad('counter');
	}
    setInterval(updateDHT, 1000);
</script>
<title>ESP32 Weather Station</title>
</head>
<body>
<center>
	<div id='main'>
		<h1>MicroPython Weather Station</h1>  
    	<h4>Web server on ESP32 | DHT values auto updates using AJAX.</h4>
		<div id='content'>
			<p>Temperature: <strong><span id='temp'>--.-</span> &deg;C</strong></p>
			<p>Humidity: <strong><span id='humi'>--.-</span> % </strong></p>
		</div>
	</div>
</center>
</body>
</html>
    """
    return html_page


def WebServer():
    # Open a socket
    # Set up the socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        
        # Socket receive()
        request = conn.recv(1024)
        print('Request:', request)

        # Handle different paths
        if '/counter' in request.decode():  # AJAX request for counter value
            response = get_counter()  # Get the updated counter

        else:  # Serve the main HTML page
            response = web_page()
            
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        
        # Socket close()
        conn.close()


