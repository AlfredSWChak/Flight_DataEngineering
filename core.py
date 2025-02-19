import part1 as pt1
import part3 as pt3


# Just printing out the tables in database for review
pt3.getTable("airlines")
pt3.printTable()

pt3.getTable("airports")
pt3.printTable()

pt3.getTable("flights")
pt3.printTable()

pt3.getTable("planes")
pt3.printTable()

pt3.getTable("weather")
pt3.printTable()

# functions that can be used to access the database in specific column
pt3.getTable_Equal("airports","faa","JFK")
pt3.printTable()

pt3.getTable_Larger("flights","distance",2000)
pt3.printTable()

pt3.getTable_Larger("planes","seats",200)
pt3.printTable()

pt3.getTable_Smaller("weather","visib",1.0)
pt3.printTable()