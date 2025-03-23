# Flight_DataEngineering

## Project Overview
This project visualizes airport data and flight information using `plotly.express` and `plotly.graph_objects`. The dataset consists of airport locations, altitudes, and time zones, and is used to generate various visualizations, including:

- A global map showing all airports.
- A US-only map filtering US-American airports.
- Flight paths from NYC to selected airports.
- Distance calculations and visualizations.
- Time zone analysis of airports.

This project is part of a larger effort to monitor and analyze flight data, leveraging libraries such as `pandas`, `numpy`, `plotly`, `seaborn`, `matplotlib` and `streamlit` for data processing and visualization.

## Project Structure
```
📂 Flight_DataEngineering
│── 📜 README.md                  # Documentation file
│── 📜 dashboard.py               # Streamlit application entry point
│── 📜 flights_database.db        # SQLite database  
├── 📂 title_pages            # Dashboard pages for Streamlit application
│ ├── 📜 delay_flights.py         # Delay-related flight analysis
│ ├── 📜 delay_weather.py         # Weather-related flight statistics & calculations
│ ├── 📜 general_airlines.py      # Weather impact analysis
│ ├── 📜 general_pages.py         # Flight visualizations (Plotly)  
│ ├── 📜 general_flights.py       # Database queries for flight data (SQLite)
│ ├── 📜 general_weathers.py      # Weather data-related visualizations for differnt seasons
│ ├── 📜 home.py                  # Home page of the dashboard
│ └── 📜 interesting.py           # Interesting flight data (maps and selected date analysis)
├── 📂 functions                  # Modular function scripts for usage in title_pages
│ ├── 📜 airlines.py              # Airline fleet analysis
│ ├── 📜 extra.py                 # Supplementary functions
│ ├── 📜 flights.py               # Flight statistics & calculations
│ ├── 📜 manipulating.py          # Database queries (SQLite)
│ ├── 📜 weather.py               # Functions for weather analysis
│ ├── 📜 wrangling.py             # Database wrangling
├── 📂 database_csv               # Exported database tables
└── 📂 .streamlit                 # Streamlit config (ignored)
```
## Key Features

### 1. 🛫 **Interactive Dashboard (Streamlit)**
- **Multi-page Navigation:**
  - 🏠 **Home**:
    - **Flights from NYC**
  - ℹ️ **General Information**:
    - **Airlines**
    - **Airports**
    - **Flights**
    - **Weather**
  - ⁉️ **Delay Analysis**:
    - **Flight Statistics**
    - **Possible Causes**
  - 📍 **Others**:
    - **Interesting Discoveries**
- **Dynamic Filters**: Date ranges, airlines, airports
- **Flight Paths**: Plotly-powered trajectory visualization

### 2. ✈️ **Data Analytics**
- **Distance Metrics**:
  - **Euclidean vs. Geodesic Distance**: Compare straight-line distance with great-circle distance.
  - **JFK-centric Distance Distributions**: Visualize distance data with respect to JFK.
- **Delay Predictors**:
  - **Weather Correlation Analysis**: Examine the impact of weather on flight delays.
  - **Airline Performance Benchmarking**: Compare airlines based on delays and other metrics.
- **Fleet Analytics**:
  - **Top 5 Aircraft Manufacturers**: Identify the most common manufacturers for flights.
  - **Route-specific Equipment Usage**: Assess aircraft used for specific routes.

### 3. 📊 **Visualization Suite**
- **Global Airport Map**: Visualize airports globally with altitude color-coding using `scatter_geo()`.
- **US Airport Filter**: Filter and visualize airports within the Continental U.S. (CONUS).
- **Multi-path Generator**: Compare JFK to LAX, ORD, and CDG flight paths.
- **Delay Maps**: Visualize delay patterns using Seaborn for temporal analysis.

### 4. 🗺️ **Distance Calculations**
- **Euclidean Distance**: Compute straight-line distance from each airport to JFK.
- **Geodesic Distance**: Accurate great-circle distance calculation.
- **Distance Distribution**: Visualize the distribution of flight distances.

### 5. **Database Queries & Flight Analysis**
- **Flight Data Retrieval**: Retrieve flight data based on parameters such as airline, airport, and date.
- **Airline Operations**: Investigate departure trends, delays, and other operational factors.
- **Aircraft Model Insights**: Assess aircraft types used on specific routes.
- **Flight Trajectory Analysis**: Analyze the frequency of aircraft models used on specific routes.
- **Airline Delay Analysis**: Compute average departure delays for each airline.
- **Delayed Flight Analysis**: Retrieve and visualize delayed flight counts by month and destination.
- **Top Aircraft Manufacturers**: Identify top 5 aircraft manufacturers for flights to specific destinations.
## Usage
### Dependencies
Ensure you have the required libraries installed before running the script:
```sh
pip install pandas numpy plotly matplotlib seaborn streamlit
```

## Running the Script

Execute the script to generate all visualizations:
```sh
  streamlit run dashoboard.py
```

## Example Usage
Visualizing Flight Paths:
```sh
  from part1 import drawMultipleLines
  drawMultipleLines(["LAX", "ORD", "CDG"], month = 1, day = 1, origin_faa = "JFK")
```
Calculating Distances:
```sh
  from flights import calculateDistances, geodesicDistance
  calculateDistances()
  geodesicDistance()
```
## Database Queries 

This project includes an SQLite database (```flights_database.db```) that provide SQL query functionality, the following table summarizes the implemented tasks:

| **Task**                              | **Implementation**                                                 | **Code Location**       |
|---------------------------------------|--------------------------------------------------------------------|-------------------------|
| **Global airport map**                | Visualize airports globally with color-coded altitude representation using Plotly | `scatter_geo()`         |
| **US-only airport map**               | Filter and display only U.S.-based airports from the dataset        | `filter_airports()`     |
| **Flight route (JFK to a single airport)** | Visualize the flight path from JFK to a selected airport           | `drawLine(faa)`         |
| **Flight route (JFK to multiple airports)** | Visualize multiple flight paths from JFK to several airports      | `drawMultipleLines(faaList, month, day, origin_faa)` |
| **Euclidean distance calculation**    | Compute the straight-line distance between airports               | `calculateDistances()`  |
| **Geodesic distance calculation**     | Calculate the accurate great-circle distance between airports     | `geodesicDistance()`    |
| **Time zones analysis**               | Analyze and visualize the time zone distribution of airports      | `analyzeTimeZone()`     |
| **Query database tables**             | Retrieve and display data from specific database tables           | `getTable(input)`       |
| **Export database tables to CSV**     | Export data from database tables into CSV format for further analysis | `export(table_name)`    |
| **Retrieve flights on a specific date** | Retrieve and display flights departing from a specific airport on a given date | `printFlightsOnDateAtAirport(month, day, airport)` |
| **Analyze flight statistics for a date** | Analyze and visualize flight statistics (e.g., delays) for a specific date | `printStatisticsOnDateAtAirport(month, day, airport)` |
| **Analyze aircraft models for routes** | Assess and visualize the types and frequencies of aircraft used on specific routes | `printPlanesStatistics(origin, dest)` |
| **Retrieve all table names**          | List all available tables within the database                      | `showAllTableNames()`   |
| **Filter data based on conditions**   | Filter data from database based on specific conditions (e.g., equals, greater than, less than) | `getTable_Equal()`, `getTable_Larger()`, `getTable_Smaller()` |
| **Flight trajectory analysis**        | Analyze and visualize the types of aircraft used on specific routes | `getPlaneTypesForRoute(origin, dest)` |
| **Airline delay analysis**            | Calculate and visualize average departure delays for each airline | `computeAverageDepartureDelay()` |
| **Delayed flight analysis**           | Identify and visualize flights that experienced significant delays | `getDelayedFlights(month_range, destination)` |
| **Top airplane manufacturers**        | Identify and visualize the top airplane manufacturers for specific destinations | `getTopManufacturers(destination)` |
| **Get Airlines List**                 | Query to fetch all airlines                                       | `getAirlines_list()`     |
| **Get All Tailnum for an Airline**    | Query to fetch all tailnum for a specific airline                 | `getAllTailnum(airline)`|
| **Get Models List for Manufacturer**  | Filter models by manufacturer                                      | `getModelsList(models_df, manufacturer)` |
| **Get Model Statistics**              | Pie chart for models, manufacturers, or years in fleet             | `getModelStatistics(scope, unique_models_df, models_df)` |
| **Get Oldest Models**                 | Get the oldest models based on the earliest year                   | `getOldestModels(count_years_df)` |
| **Get Youngest Models**               | Get the youngest models based on the latest year                   | `getYoungestModels(count_years_df)` |
| **Busiest Routes**                    | Retrieve the top 5 busiest routes based on flight count            | `busiest_routes()`      |
| **Weather Impact on Delays**          | Analyze the impact of weather on flight delays per month           | `weather_impact_on_delays()` |
| **Weather data retrieval by time hour**    | Retrieve weather data (e.g., wind direction, wind speed, visibility) for specific hours and airports.              | `getTimeHour_df(origin, time_hour_list)` |
| **Flight delay calculation**                | Calculate the average departure and arrival delays for a specific origin and destination airport.                  | `averageDelay(origin, dest)` |
| **Flight frequency per month**             | Calculate and visualize the average number of flights per month for a specific origin and destination airport.      | `flightsPerMonth(origin, dest)` |
| **Flight frequency per day**               | Calculate the average number of flights per day for a specific origin and destination airport across months.        | `flightsPerDay(origin, dest)` |
| **Non-delayed flights dot product**        | Calculate the dot product of wind speed, flight speed, and direction for non-delayed flights to evaluate wind impact. | `nonDelayDotProduct(start_month, end_month, origin, dest)` |
| **Delayed flights dot product**            | Calculate the dot product for delayed flights and assess wind speed, direction, and other factors affecting delays.   | `delayDotProduct(start_month, end_month, origin, dest)` |
| **Flight direction angle calculation**     | Calculate the angle between the flight's direction and the wind direction.                                           | `getAngleBetween(origin, dest)` |
| **Retrieve all destinations for origin**   | Get a list of all possible destinations for a given origin airport.                                                  | `get_all_destinations(origin)` |
| **Flight count by month for a specific origin** | Count the number of flights per month for a specific origin airport.                                               | `flightsPerMonthByOrigin(origin)` |
| **Total delays per month for an origin**   | Calculate the total departure and arrival delays per month for a specific origin airport.                           | `totalDelayPerMonthByOrigin(origin)` |
| **Weather data analysis by month**    | Retrieve and visualize hourly weather data for a specific airport, including wind speed, wind gust, and visibility | `getMonth(season)`      |
| **Hourly weather averages**          | Calculate and visualize the average weather conditions (e.g., wind speed, gust, visibility) by hour for a specified airport and month range | `hourlyAverage(airport, month_list)` |
| **Flight direction calculation**      | Classify flight directions based on angles between airports (e.g., Same, Right, Opposite, Left) | `count_direction(flights_df)` |
| **Get Tailnum Planes**                | Fetches details of planes based on a list of tail numbers                                        | `getTailnumPlanes(tailnum_list)` |
| **Top Five Planes**                   | Retrieves the top five planes based on the number of flights departing from a given airport     | `top_five_planes(flights_df)` |
| **Flight Data Preprocessing**         | Preprocesses flight data for analysis, including handling missing values and formatting data    | `preprocess_flight_data(flights_df)` |
| **Calculate Flight Delays**           | Calculates average flight delays for different airport routes                                    | `calculate_flight_delays(flights_df)` |
## Future Enhancements
- Integrating flight data of real-time data.
- Improving visualization aesthetics.
- Enhanced database queries and analytics.
- Flight delay predictions.
- Expanded analysis on weather impact on flights, including other weather information, such as raining, snowing.

## Contributors
Group Flights 10
Alfred, Adele, Duncan, Lan
```
