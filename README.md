# car-db

### Funcitionality
Database based on two types of file:
- List of records file
    - Each line - one record file
- Records file
    - file with special structure representing one record in DB.

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
 
  
