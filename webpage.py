# Function for creating the
# web page to be displayed
def web_page():
    html_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Dashboard</title>
    <style>
        /* Reset */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        /* Page layout */
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(to right, #74ebd5, #acb6e5);
            color: #333;
        }

        /* Weather card */
        .weather-card {
            background-color: #fff;
            border-radius: 8px;
            padding: 20px;
            max-width: 800px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        .weather-card h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }

        .location {
            font-size: 1.2em;
            color: #666;
            margin-bottom: 10px;
        }

        .temperature {
            font-size: 3em;
            font-weight: bold;
            color: #333;
        }

        .description {
            font-size: 1.2em;
            margin: 10px 0;
            color: #888;
        }

        .details {
            display: flex;
            justify-content: space-between;
            font-size: 0.9em;
            color: #555;
        }

        .details div {
            text-align: center;
        }

        .refresh-button {
            background: #74ebd5;
            color: #333;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 15px;
            transition: background 0.3s;
        }

        .refresh-button:hover {
            background: #67d4c5;
        }
    </style>
</head>
<body>

    <!-- Weather Card Structure -->
    <div class="weather-card" id="weatherCard">
        <h1>Weather Info</h1>
        <div class="location" id="location">London</div>
        <div class="temperature" id="temperature">25.75C</div>
        <div class="description" id="description">overcast clouds</div>
        
        <!-- Weather Details -->
        <div class="details">
            <div>
                <p>Humidity</p>
                <p id="humidity">57%</p>
            </div>
            <div>
                <p>Wind</p>
                <p id="wind">32km/h</p>
            </div>
        </div>

        <!-- Refresh Button -->
        <button class="refresh-button" onclick="fetchWeather()">Refresh</button>
    </div>

    <!-- JavaScript for fetching weather data -->
    <script>
        var ajaxRequest = new XMLHttpRequest();
        async function ajaxLoad(ajaxURL)
        {     
            ajaxRequest.open('GET',ajaxURL,true);
		    ajaxRequest.onreadystatechange = function()
            {
                if(ajaxRequest.readyState == 4 && ajaxRequest.status==200)
		        {
                    let ajaxResult = ajaxRequest.responseText;
                    let tmpArray = ajaxResult.split("|");
                    document.getElementById('location').innerText = tmpArray[0];
                    document.getElementById('temperature').innerText = tmpArray[1] + "°C";
                    document.getElementById('description').innerText = tmpArray[2];
                    document.getElementById('humidity').innerText = tmpArray[3] + "%";
                    document.getElementById('wind').innerText = tmpArray[4] + "km/h";
                }
            }
            ajaxRequest.send();
        }
        function updateWeather()
	    {
		    ajaxLoad('weather');
	    }
        setInterval(updateWeather, 2000);
    </script>
</body>
</html>

    """
    return html_page
