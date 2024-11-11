# Function for creating the
# web page to be displayed
def web_page():
    html_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather, Map & Chart Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> <!-- Chart.js library -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" /> <!-- Leaflet CSS -->
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script> <!-- Leaflet JS -->
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
            padding: 20px;
        }

        .container {
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
        }

        /* Card styles */
        .card {
            background-color: #fff;
            border-radius: 8px;
            padding: 30px; /* Increased padding for larger cards */
            width: 450px; /* Increased width by 50% */
            text-align: center;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* Increased shadow */
        }

        /* Weather card styles */
        .weather-card h1 {
            font-size: 2.5em; /* Increased font size */
            margin-bottom: 15px;
        }

        .location {
            font-size: 1.5em; /* Increased font size */
            color: #666;
            margin-bottom: 15px;
        }

        .temperature {
            font-size: 3.5em; /* Increased font size */
            font-weight: bold;
            color: #333;
        }

        .description {
            font-size: 1.5em; /* Increased font size */
            margin: 15px 0;
            color: #888;
        }

        .details {
            display: flex;
            justify-content: space-between;
            font-size: 1.2em; /* Increased font size */
            color: #555;
        }

        .details div {
            text-align: center;
        }

        .refresh-button {
            background: #74ebd5;
            color: #333;
            border: none;
            padding: 15px 25px; /* Larger button */
            border-radius: 5px;
            cursor: pointer;
            margin-top: 20px;
            transition: background 0.3s;
        }

        .refresh-button:hover {
            background: #67d4c5;
        }

        /* Map card styles */
        .map-card h2 {
            font-size: 2em; /* Increased font size */
            margin-bottom: 20px;
        }

        .map-container {
            width: 100%;
            height: 300px; /* Increased height */
            border-radius: 8px;
            overflow: hidden;
        }

        /* Chart card styles */
        .chart-card h2 {
            font-size: 2em; /* Increased font size */
            margin-bottom: 20px;
        }

        .chart-container {
            width: 100%;
            height: 300px; /* Increased height */
        }

        /* Input field styles */
        .city-input {
            width: 70%;
            padding: 10px;
            font-size: 1em;
            margin-top: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }

        .search-button {
            width: 25%;
            padding: 10px;
            font-size: 1em;
            background-color: #74ebd5;
            border: none;
            border-radius: 5px;
            color: #333;
            cursor: pointer;
            margin-top: 10px;
        }

        .search-button:hover {
            background-color: #67d4c5;
        }
    </style>
</head>
<body>

    <div class="container">
        <!-- Weather Card Structure -->
        <div class="card weather-card" id="weatherCard">
            <h1>Weather Info</h1>
            <div class="location" id="location">Loading...</div>
            <div class="temperature" id="temperature">--°C</div>
            <div class="description" id="description">--</div>
            
            <!-- Weather Details -->
            <div class="details">
                <div>
                    <p>Humidity</p>
                    <p id="humidity">--%</p>
                </div>
                <div>
                    <p>Wind</p>
                    <p id="wind">-- km/h</p>
                </div>
            </div>
            <!-- City Input and Search Button -->
            <input type="text" class="city-input" id="cityInput" placeholder="Enter city name" />
            <button class="search-button" onclick="updateWeather()">Search</button>
        </div>

        <!-- Map Card Structure -->
        <div class="card map-card">
            <h2>Location Map</h2>
            <div class="map-container" id="map"></div>
        </div>

        <!-- Chart Card Structure -->
        <div class="card chart-card">
            <h2>Temperature & Humidity Chart</h2>
            <div class="chart-container">
                <canvas id="weatherChart"></canvas>
            </div>
        </div>
    </div>

    <!-- JavaScript for fetching weather data -->
    <script>
        let lat = 0, lon = 0;
        let map, marker;  // Leaflet map and marker variables
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
                    lon = Number(tmpArray[5]);
                    lat = Number(tmpArray[6]);
                }
            }
            ajaxRequest.send();
        }
        function updateWeather()
	    {
            const cityInput = document.getElementById('cityInput');
            const city = cityInput.value || 'London';  // Default to London if no input
            let url = 'weather&city:' + city;
		    ajaxLoad(url);
		    // Delay map loading until container has full dimensions
                setTimeout(() => {
                loadMap();
            }, 3500);
		    
	    }
	    function loadMap()
	    {
            // Initialize map only once, update marker position afterward
            if (!map) {
                map = L.map('map').setView([lat, lon], 10);

                // Set up the OpenStreetMap tiles
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 18,
                    attribution: '© OpenStreetMap'
                }).addTo(map);

                // Add a marker for the location
                marker = L.marker([lat, lon]).addTo(map);
            } else {
                map.setView([lat, lon], 10);  // Update map view
                marker.setLatLng([lat, lon]); // Update marker position
            }
        }
	    window.onload = updateWeather;
        setInterval(updateWeather, 60000);
    </script>
</body>
</html>

    """
    return html_page
