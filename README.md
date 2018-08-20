# Car Rental Database

### General description
Database based on two types of file:
- List of records file
    - Each line - one record file
- Records file
    - file with special structure representing one record in DB.

Program works as a reservation system for car rental company database. The program can search the database and output nice tables with all information about cars.
User shall make a reservation for a car. Program can exit on user input.

The database files will be provided for the student.

The program is user friendlyu - everything user needs is printed out.

#### Search capabilities
- compares keys (categories ex.:  brand, model..) and values entered by user with keys and values in database. 
- user shall decide how entered and database values are compared
    - example 1: When searching for specific brand user inputs: brand, actual brand name (ex: Mazda), == (user input and database value should be equal)
    - example 2: When searching cars with more than 100kW of power. Intput: power, 100, > (user input greater then datase value)  
- user can perform search based on multiple conditions 

#### Print capabilites
- Program outputs search results **or** all availible cars
- printing is done via formated strings
- output looks like table
- when multiple cars are selected, on output it can be easily distinguished between them
- output contains all information about car found in database + it's ID

#### List of records file structure
- one line one file
- files shall by named by numbers which represents 

#### Record file structure
 - key goes first
 - delimeter btw key and value is '='
 - delimeter is straight connected to key and value - no spaces
 - max depth 1 - can include only 1 nested 'dict'
 - key of nested 'dict' is without value, delim is needed
 - nested kye=value are on separate rows indented by 4 spaces.
 
  
