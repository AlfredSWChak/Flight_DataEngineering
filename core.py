import part1 as pt1
import part3 as pt3
import part4 as pt4

# Plot all the airports inside the database
pt1.showAllAirports()

# Plot all the airports with different time zones and a barplot 
pt3.advanced_time_zones()

# Can be used to plot a barplot according to user input (i.e.:['planes', 'manufacturer'])
pt3.barplot_frequency('planes', 'manufacturer')

# Plot the distribution of altitude of airports
pt3.analyze_altitude()

# Plot a map contains all destinations of flights on that day from specific airport
pt3.printFlightsOnDateAtAirport(2, 21, 'LGA') 

# Returns statistics for that day, how many flights,how many unique destinations, which destination is visited most often
pt3.printStatisticsOnDateAtAirport(2, 22, 'JFK')

# Returns how many times each plane type was used for that flight trajectory
# Takes long times to run the result (should be revised)
pt3.printPlanesStatistics('JFK','ATL')

# Investigate the relationship between the distance of a flight and the arrival delay time
# Plot a scatter plot and a histogram (but the scale of histogram should be revised)
pt3.arrivalDelayPlot()

# Plot a barplot about departure delay per flight for each of the airlines
pt3.departureDelayPlot()

# Returns the amount of delayed flights to that destination.
pt3.amongOfDelayFlights(7, 9, 'FLL')

# pt3.planes_speed()

# 
# pt3.compute_wind_direction_from_NYC()

# pt4.check_na_flights()

# pt4.drop_duplicates_except(['flight'])

# pt4.convert_datetime()

# pt4.local_arrival_time()