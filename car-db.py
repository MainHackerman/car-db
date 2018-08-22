# Reads a given file
def readfile(filename):
    s = open(filename)
    content = s.read()
    s.close()
    return content


# Reads file with car info and create a dictionary from that
def decode(filename):
    decoded = {}
    raw = readfile(filename)
    rows = raw.split('\n')
    dictionary = ''
    for pair in rows:

        if pair:
            key = pair.split('=')[0]
            value = pair.split('=')[1]
            if not value:
                decoded.update({key: {}})
                dictionary = key
            elif key[0] == ' ' and dictionary:
                decoded.get(dictionary).update({key[4:]: value})
            else:
                decoded.update({key: value})
                dictionary = ''

    return decoded


# Takes file with car IDs and creates dictionaries with keys representing ÍDs and values dictionaries including car info as returned by decode()
def readDB(db_file):
    db = {}
    raw = readfile(db_file)
    rows = raw.split('\n')
    for row in rows:
        if row:
            db.update({row: decode('files/' + row + '.txt')})
    return db


# Checks if given ID is in ID file
def IDinDB(int_id, db_filename):
    f = open(db_filename)
    for row in f:
        if row == '\n':
            continue
        if int(row) == int_id:
            f.close()
            return True
    else:
        f.close()
        return False


# Adds ID to a file
def addID(int_id, db_filename):
    f = open(db_filename, 'a')
    f.write('\n' + str(int_id))
    f.close()


# Removes ID from a file
def delID(int_id, db_filename):
    f = open(db_filename)
    cont = f.read().split('\n')
    f.close()
    cont.remove(str(int_id))

    f = open(db_filename, 'w')
    for item in cont:
        f.write(str(item) + '\n')
    f.close()


# Moves ID from one ID file to another, checks if the ID is already present in taget file or if ID even exists
def rentCar(int_id, rented_db_filename, not_rented_db_filename):
    if IDinDB(int_id, rented_db_filename):
        print('Car is rented')
        return False
    elif not IDinDB(int_id, not_rented_db_filename):
        print('ID is not valid')
        return False

    addID(int_id, rented_db_filename)
    delID(int_id, not_rented_db_filename)

    return True


# Compares two given values with given comparison sign
def compare(val1, val2, symbol):
    # <,>,<=,>=, ==
    if val1.isdigit() and val2.isdigit():
        val1, val2 = float(val1), float(val2)
    if symbol == '<':
        return val1 < val2
    elif symbol == '>':
        return val1 > val2
    elif symbol == '<=':
        return val1 <= val2
    elif symbol == '>=':
        return val1 >= val2
    elif symbol == '==':
        return val1 == val2
    else:
        print('wrong symbol')
        return False


# Returns list of car IDs which comply given condition
def getCar(key, value, comp_symbol, db_dict):
    ID_list = []
    for car in db_dict.items():
        for car_item in car[1].items():
            if type(car_item[1]) == type({}):
                for car_nested_item in car_item[1].items():
                    if car_nested_item[0] == str(key) and compare(car_nested_item[1], str(value), comp_symbol):
                        ID_list.append(car[0])
            if car_item[0] == str(key) and compare(car_item[1], str(value), comp_symbol):
                ID_list.append(car[0])
    return ID_list


# Returns list of car IDs which comply given multiple conditions
def getMore(db_dict, conditions):
    # One condition shall be tuple including key, value, comp sign
    matches = []
    for condition in conditions:
        if not condition:
            continue
        matches.append(set(getCar(*condition, db_dict)))
    if not matches:
        return []

    return list(set.intersection(*matches))


# Retruns list of list of tuples. Each nested list represents one car, each nested tuple in this list includes key and its value of a "car" dict
def getFormat(list_result, db_dict):
    to_format = []
    for result in list_result:
        car = []
        car.append(tuple(['ID', result]))
        car_record = db_dict.get(result)
        for item in car_record.items():
            if type(item[1]) == type({}):
                car.append(tuple([item[0], '']))
                for nested_item in item[1].items():
                    car.append(nested_item)
                continue

            car.append(item)
        to_format.append(car)

    return to_format


# Returns nice formated string for printing. Constructed from given car ID list.
def printResult(list_result, db_dict):
    cont_to_format = getFormat(list_result, db_dict)
    print(cont_to_format)
    beg = ' RESULT OF YOUR SEARCH:\n' + 45*'='+'\n'
    row_to_format = '|{: ^20} : {: ^20}|'
    cont_str = ''
    end = 'THANK YOU FOR USING OUR SYSTEM'
    for lst in cont_to_format:
        for pair in lst:
            cont_str = cont_str + row_to_format.format(*pair) + '\n'
        cont_str = cont_str + 45*'='+ '\n'

    return beg + cont_str + end

# BODY OF THE PROGRAM

db = readDB('files/not_rented.txt')

options = ['SEARCH', 'RENT', 'QUIT', 'SHOW ALL']

while True:
    print('WLECOME TO CAR RENTAL COMPANY')
    print('YOU CAN: SHOW ALL, SEARCH, RENT, QUIT')
    pick = input('STATE YOUR DECISION: ').upper()

    if pick == options[0]:
        comp_items = ['ITEM', 'VALUE', 'COMPARISON SING']
        tuples = []
        while True:
            tup = ()
            inp = 0
            print('SEARCHING OUR DATABASE.\nEnter in which category do you search, what you search and how should it compare to value in database.')
            print('Prices are displayed per day, consumtion in liters per 100km.')
            print('To exit and confirm search leave empty space (do not enter anything) and press enter.')
            for item in comp_items:
                inp = [input('Enter ' + item + ' :\n')]
                if not inp[0]:
                    break
                elif len(inp) == 2 and not inp[2]:
                    break
                elif len(inp) == 3 and not inp[2]:
                    break
                tup = tup + tuple(inp)
            tuples.append(tup)
            if not len(tup) == 3:
                del tuples[-1]
                break
        s_result = getMore(db, tuples)
        print(printResult(s_result, db))

    elif pick == options[1]:
        print('You decided to rent a car, great choice!')
        rent_id = input('Enter ID of car: ')

        if not rent_id.isdigit():
            print('Input is not a number')
            continue

        if rentCar(int(rent_id), 'files/rented.txt','files/not_rented.txt'):
            print('CONGRATULATIONS! YOU HAVE RESERVED CAR NUMBER ', rent_id)
        pass

    elif pick == options[2]:
        print('THANK YOU FOR USING OUR SERVICES, GOOD BYE')
        break
    elif pick == options[3]:
        print('ALL OUR CARS:')
        print(printResult(list(db.keys()), db))

    else:
        print('Wrong choice - not in menu.')