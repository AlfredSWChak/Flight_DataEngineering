# Flight_DataEngineering

## Project Overview
This project visualizes airport data and flight information using `plotly.express` and `plotly.graph_objects`. The dataset consists of airport locations, altitudes, and time zones, and is used to generate various visualizations, including:

- A global map showing all airports.
- A US-only map filtering American airports.
- Flight paths from NYC to selected airports.
- Distance calculations and visualizations.
- Time zone analysis of airports.

This project is part of a larger effort to monitor and analyze flight data, leveraging `pandas`, `numpy`, `plotly`, `seaborn`, and `matplotlib` for data processing and visualization.

## Part 1: 📂Project Structure
```
📂 flight-monitoring
│── 📜 README.md                 # Documentation file  
│── 📜 part1.py                  # Flight visualizations (Plotly)  
│── 📜 part3.py                  # Database queries (SQLite)  
│── 📜 core.py                   # Core functions  
│── 📜 flights_database.db       # SQLite database  
│── 📜 airports_original.csv     # Airport dataset  
│── 📜 (More files coming...)  
```
## Part * : ✈️ Features
### 1. Airport Maps
- **Global Airport Map**: Plots all airports from the dataset.
- **US Airport Map**: Filters and displays only US airports.
- **Altitude Color Coding**: Airports are color-coded based on altitude.

### 2. Flight Path Visualization
- **Single Airport Flight Path**: A function to draw a flight path from NYC to a specified airport.
- **Multiple Flight Paths**: Extends the function to accept a list of airport FAA codes and draw multiple flight paths from NYC.

### 3. Distance Calculations
- **Euclidean Distance**: Computes the Euclidean distance from each airport to JFK.
- **Geodesic Distance**: Calculates a more accurate great-circle distance.
- **Distance Distribution**: Visualizes the distribution of distances.

### 4. Time Zone Analysis
- **Time Zone Graph**: Analyzes and visualizes airports based on their time zones.

## Usage
### Dependencies
Ensure you have the required libraries installed before running the script:
```sh
pip install pandas numpy plotly matplotlib seaborn






## Running the Script

Execute the script to generate all visualizations:
  python flights.py

## Example Usage
Visualizing Flight Paths:
  from flights import drawMultipleLines
  drawMultipleLines(["LAX", "ORD", "CDG"])

Calculating Distances:
  from flights import calculateDistances, geodesicDistance
  calculateDistances()
  geodesicDistance()


## Future Enhancements
- Integrating flight data from a database.
- Adding real-time flight tracking.
- Improving visualization aesthetics.

## Contributors
Group FLights 10
Lan, Alfred, Adele, Duncan
```
## Part *: Database Queries 

Goal: Use ```flights_database.db``` to provide SQL query functionality, implementling the following tasks:

## Part *: Data Analysis Tasks

| Task | Implementation | Code Location |
|------|--------------|--------------|
| **Global airport map** | Plotly `scatter_geo()` | `part1.py` |
| **US-only airport map** | Filter `airports_original.csv` data | `part1.py` |
| **Draw JFK to a single airport route** | `drawLine(faa)` | `part1.py` |
| **Draw JFK to multiple airports routes** | `drawMultipleLines(faaList, month, day, origin_faa)` | `part1.py` |
| **Compute Euclidean distance** | `calculateDistances()` | `part1.py` |
| **Compute geodesic (spherical) distance** | `geodesicDistance()` | `part1.py` |
| **Analyze airport time zones** | `analyzeTimeZone()` | `part1.py` |
| **Query database tables** | `getTable(input)` | `part2.py` |
| **Export database tables to CSV** | `export(table_name)` | `part2.py` |
| **Retrieve flights on a specific date** | `printFlightsOnDateAtAirport(month, day, airport)` | `part2.py` |
| **Analyze flight statistics for a date** | `printStatisticsOnDateAtAirport(month, day, airport)` | `part2.py` |
| **Analyze aircraft models for a route** | `printPlanesStatistics(origin, dest)` | `part2.py` |

## Future Enhancements

## References
Plotly Documentation
