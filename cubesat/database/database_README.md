# Database

 ## Table Design

| Top Left Latitude | Top Left Longitude | Average Brightness | Lights On/Off                | Year | Month | Day | Hour     | Minute     | Second     |
|-------------------|--------------------|--------------------|------------------------------|------|-------|-----|----------|------------|------------|
| Float             | Float              | Float              | Float                        | Int  | Int   | Int | Int      | Int        | Int        |
| Latitude          | Longitude          | Average Brightness | 0-1 Percent of Bright Pixels | Year | Month | Day | GPS Hour | GPS Minute | GPS Second |


## API
### create ###  
Call once to create the database

### write ###  
Args:
- data: a list following the table format

Returns:
- Nothing

Post-Condition:  
- The data gets stored into the database

### get_filter ###  
Args:
- lat_long: String of latitude and longitude, formatted as *latitude "space" longitude*
  - eg: "123.456 789.010"

Returns:
- A list of lists with all stored instances of the given coordinates

### get  ###
Returns:
- A list of lists of all stored data in the database

### getID ##
Args:
- Lat: latitude of location
- Long: longitude of location

Returns:
- A string containing the lat_long id, formatted a *latitude "space" longitude*