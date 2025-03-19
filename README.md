# Flight_DataEngineering

## Project Overview
This project visualizes airport data and flight information using `plotly.express` and `plotly.graph_objects`. The dataset consists of airport locations, altitudes, and time zones, and is used to generate various visualizations, including:

- A global map showing all airports.
- A US-only map filtering American airports.
- Flight paths from NYC to selected airports.
- Distance calculations and visualizations.
- Time zone analysis of airports.

This project is part of a larger effort to monitor and analyze flight data, leveraging `pandas`, `numpy`, `plotly`, `seaborn`, and `matplotlib` for data processing and visualization.

## Project Structure
```
📂 flight-monitoring
│── 📜 README.md                 # Documentation file  
│── 📜 part1.py                  # Flight visualizations (Plotly)  
│── 📜 part3.py                  # Database queries (SQLite)
│── 📜 part4.py                  # Streamlit application
│── 📜 core.py                   # Core functions  
│── 📜 flights_database.db       # SQLite database  
│── 📜 airports_original.csv     # Airport dataset
── 📂 functions                  # Modular function scripts  
│    ├── airlines.py             # Airline-related functions  
│    ├── flights.py              # Flight statistics functions   
│── 📜 (More files coming...)  
```
## Features
### 1. Interactive Web Application(Streamlit)
- **General Airport Information**: Displays airport locations, altitude, and time zones.
- **General Airline Information**: Analyze airline operations, aircraft models, and fleet statistics.
- **General Flight Information**: Retrieves flight routes, delays, and usage statistics.
- **Flight Statistics on Specific Days**: Analyzes daily flight trends at major NYC sirports.
- **Delayed Flight Analysis**: Compute the number of delayed flights within a selected date range.
### 2. Airport Maps & Visualizations
- **Global Airport Map**: Plots all airports from the dataset.
- **US airport Map**: Fliters and displays only US airports.
- **Altitude Color Coding**: Airports are color-coded based on altitude.

### 3. Flight Path Visualization
- **Single Airport Flight Path**: Show a flight path from JFK to other specified airports on a single day.
- **Multiple Flight Paths**:

### 4. Distance Calculations
- **Euclidean Distance**: Computes the Euclidean distance from each airport to JFK.
- **Geodesic Distance**: Calculates a more accurate great-circle distance.
- **Distance Distribution**: Visualizes the distribution of distances.

### 5. Databse Queries & Flight Analysis
- ** Retrieve flight data: Query flights based on various parameters.
- ** Analyze airline operations: Investigate departure trends delays.
- ** Aircraft model insights: Assess aircraft usage for different rountes.
- ** Flight trajectory analysis: Determine how many times each plane type was used for a specific route.
- ** Airline delay analysis: Compute the average departure delay per airline and visualize in a bar plot.
- ** Delay flight analysis: Retrieve the numberof delayed flights for a given range of months and destination.
- ** Top airplane manufacturers: Identidy the top 5 airplane manufacturers for flights departing to a specified destination.

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
