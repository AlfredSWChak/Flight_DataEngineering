# Flight_DataEngineering

## Project Overview
This project visualizes airport data and flight information using `plotly.express` and `plotly.graph_objects`. The dataset consists of airport locations, altitudes, and time zones, and is used to generate various visualizations, including:

- A global map showing all airports.
- A US-only map filtering American airports.
- Flight paths from NYC to selected airports.
- Distance calculations and visualizations.
- Time zone analysis of airports.

This project is part of a larger effort to monitor and analyze flight data, leveraging `pandas`, `numpy`, `plotly`, `seaborn`, `matplotlib` and `streamlit` for data processing and visualization.

## Project Structure
```
📂 flight-monitoring
│── 📜 README.md                 # Documentation file
│── 📜 home.py                   # Streamlit application entry point
│── 📜 part1.py                  # Flight visualizations (Plotly)  
│── 📜 part3.py                  # Database queries (SQLite)
│── 📜 part4.py                  # Streamlit application
│── 📜 core.py                   # Core functions  
│── 📜 flights_database.db       # SQLite database  
│── 📜 airports_original.csv     # Airport dataset
── 📂 functions                  # Modular function scripts  
│ ├── 📜 airlines.py             # Airline fleet analysis
│ ├── 📜 flights.py              # Flight statistics & calculations
│ ├── 📜 weather.py              # Weather impact analysis
│ └── 📜 duncan_function.py      # Custom route analytics
├── 📂 database_csv              # Exported database tables
├── 📂 .streamlit                # Streamlit config (ignored)
└── 📜 part1.py                  # Flight path visualizations
📜 part3.py                      # Advanced SQL queries
📜 part4.py                      # Streamlit UI enhancements
📜 extra.py                      # Utility functions 

```
## Key Features

###1. 🛫 **Interactive Dashboard (Streamlit)**
Multi-page Navigation:
Home: System overview
General: Airport/airline metadata
Delay: Historical delay patterns
Dynamic Filters: Date ranges, airlines, airports
Flight Paths: Plotly-powered trajectory visualization

###2. ✈️ **Data Analytics**
Distance Metrics:
Euclidean vs Geodesic distance comparisons
JFK-centric distance distributions
Delay Predictors:
Weather correlation analysis
Airline performance benchmarking
Fleet Analytics:
Top 5 aircraft manufacturers
Route-specific equipment usage

###3. ✈️ **Data Analytics**
Distance Metrics:
Euclidean vs Geodesic distance comparisons
JFK-centric distance distributions
Delay Predictors:
Weather correlation analysis
Airline performance benchmarking
Fleet Analytics:
Top 5 aircraft manufacturers
Route-specific equipment usage

###4. 📊 **Visualization Suite**
Global Airport Map: scatter_geo() with altitude color-coding
US Airport Filter: Geo-fenced CONUS visualization
Multi-path Generator: Compare JFK→LAX, JFK→ORD, and JFK→CDG trajectories
Delay Heatmaps: Seaborn-based temporal patterns

###5. 🗺️ **Distance Calculations**
Euclidean Distance: Computes distance from each airport to JFK.
Geodesic Distance: More accurate great-circle distance calculation.
Distance Distribution: Visualizes the distribution of distances.

###6. **Database Queries & Flight Analysis**
Flight Data Retrieval: Query flights based on parameters like airline, airport, and date.
Airline Operations: Investigate departure trends and delays.
Aircraft Model Insights: Assess aircraft usage per route.
Flight Trajectory Analysis: Analyze frequency of aircraft types used on specific routes.
Airline Delay Analysis: Compute average departure delay per airline (bar plot).
Delay Flight Analysis: Retrieve delayed flight counts by month and destination.
Top Aircraft Manufacturers: Identify the top 5 manufacturers for flights to a specified destination.

## Usage
### Dependencies
Ensure you have the required libraries installed before running the script:
```sh
pip install pandas numpy plotly matplotlib seaborn streamlit altair
```

## Running the Script

Execute the script to generate all visualizations:
```sh
  stream run home.py
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

| Task | Implementation | Code Location |
|------|--------------|--------------|
| **Global airport map** | Plotly `scatter_geo()` | `part1.py` |
| **US-only airport map** | Filter `airports_original.csv` data | `part1.py` |
| **Flight route(JFK to a single airport)** | `drawLine(faa)` | `part1.py` |
| **Flight route(JFK to multiple airports)** | `drawMultipleLines(faaList, month, day, origin_faa)` | `part1.py` |
| **Euclidean distance calculation** | `calculateDistances()` | `part1.py` |
| **Geodesic distance calculation** | `geodesicDistance()` | `part1.py` |
| **Time zones analysis** | `analyzeTimeZone()` | `part1.py` |
| **Query database tables** | `getTable(input)` | `part2.py` |
| **Export database tables to CSV** | `export(table_name)` | `part2.py` |
| **Retrieve flights on a specific date** | `printFlightsOnDateAtAirport(month, day, airport)` | `part2.py` |
| **Analyze flight statistics for a date** | `printStatisticsOnDateAtAirport(month, day, airport)` | `part2.py` |
| **Analyze aircraft models for routes** | `printPlanesStatistics(origin, dest)` | `part2.py` |
| **Retrieve all table names** | `showAllTableNames()` | `part2.py`|
| **Fliter data based on conditions** | `getTable_Equal()`, `getTable_Larger()`, `getTable_Smaller()` | `part2.py`|
| **Flight trajectory analysis** | `getPlaneTypesForRoute(origin, dest)` | `part2.py`|
| **Airline delay analysis** | `computeAverageDepartureDelay()` | `part2.py`
| **Delayed flight analysis** | `getDelayedFlights(month_range, destination)`| `part2.py`|
| **Top airplane manufacturers** | `getTopManufacturers(destination)`| `part2.py`|

## Future Enhancements
- Integrating flight data of real-time data.
- Improving visualization aesthetics.
- Enhanced database queries and analytics.
- Flight delay predictions.
- Expanded analysis on weather impact on flights.

## Contributors
Group FLights 10
Alfred, Adele, Duncan, Lan
```

## References
Plotly Documentation
SQLite Documentation
Seaborn Visualization Guide
