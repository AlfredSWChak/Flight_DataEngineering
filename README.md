# Flight_DataEngineering

## Project Overview
This project visualizes airport data and flight information using `plotly.express` and `plotly.graph_objects`. The dataset consists of airport locations, altitudes, and time zones, and is used to generate various visualizations, including:

- A global map showing all airports.
- A US-only map filtering American airports.
- Flight paths from NYC to selected airports.
- Distance calculations and visualizations.
- Time zone analysis of airports.

This project is part of a larger effort to monitor and analyze flight data, leveraging `pandas`, `numpy`, `plotly`, `seaborn`, and `matplotlib` for data processing and visualization.

## Features
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

