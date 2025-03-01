import part1 as pt1
import part3 as pt3

# functions that can be used to access the database in specific column
pt3.getTable_Equal("airports","faa","JFK")
# pt3.printTable()

pt3.getTable_Larger("flights","distance",2000)
# pt3.printTable()

pt3.getTable_Larger("planes","seats",200)
# pt3.printTable()

pt3.getTable_Smaller("weather","visib",1.0)
# pt3.printTable()

# Only 3 options :['EWR', 'LGA', 'JFK']
# Input parameters: [month, day, origin]
# pt3.printFlightsOnDateAtAirport(2, 21, 'LGA') 

# pt3.printStatisticsOnDateAtAirport(2, 22, 'JFK')

# pt3.printPlanesStatistics('JFK','ATL')

# pt3.arrivalDelayPlot()

# pt3.departureDelayPlot()

# pt3.amongOfDelayFlights(7, 9, 'FLL')

# pt3.planes_speed()

pt3.compute_wind_direction_from_NYC()