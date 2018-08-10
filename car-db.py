def readfile(filename):
    s = open(filename)
    content = s.read()
    s.close()
    return content


def decode(filename):
    decoded = {}
    raw = readfile(filename)
    rows = raw.split('\n')
    dictionary = {}
    for pair in rows:

        if pair:
            if not pair.split('=')[1]:
                decoded[pair.split('=')[0]] = {}
                dictionary = pair.split('=')[0]
            elif pair.split('=')[0][0] == ' ' and dictionary:
                polozky = pair.split('=')
                decoded[dictionary].update({polozky[0][4:]: polozky[1]})
            else:
                polozky = pair.split('=')
                decoded[polozky[0]] = polozky[1]
                dictionary = {}

    return decoded


def readDB(db_file):
    db = {}
    f = open(db_file)
    rows = []
    for row in f:
        if row[-1] == '\n':
            rows.append(row[:-1])
        else:
            rows.append(row)
    f.close()
    for row in rows:
        if row != '\n':
            db.update({row: decode(row + '.txt')})
    return db


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


def addID(int_id, db_filename):
    f = open(db_filename, 'a')
    f.write('\n' + str(int_id))
    f.close()


def delID(int_id, db_filename):
    f = open(db_filename)
    cont = f.read().split('\n')
    f.close()
    cont.remove(str(int_id))

    f = open(db_filename, 'w')
    for item in cont:
        f.write(str(item) + '\n')
    f.close()


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


def compare(val1, val2, symbol):
    #<,>,<=,>=, ==
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


def getCar(key, value, comp_symbol, db_dict):
    ID_list = []
    for car in db_dict.items():
        for car_item in list(car)[1].items():
            if type(car_item[1]) == type({}):
                for car_nested_item in car_item[1].items():
                    if car_nested_item[0] == str(key) and compare(car_nested_item[1], str(value), comp_symbol):
                        ID_list.append(list(car)[0])
            if car_item[0] == str(key) and compare(car_item[1], str(value), comp_symbol):
                ID_list.append(list(car)[0])
    return ID_list


def getMore(db_dict, conditions):
    #One condition shall be tuple including key, value, comp sign
    matches = []
    for condition in conditions:
        if not condition:
            break
        matches.append(set(getCar(condition[0], condition[1], condition[2], db_dict)))

    return list(set.intersection(*matches))


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


def printResult(list_result, db_dict):
    cont_to_format = getFormat(list_result, db_dict)
    beg = ' VYSLEDEK VASEHO HLEDANI:\n' + 45*'='+'\n'
    row_to_format = '''|{: ^20} : {: ^20}|'''
    cont_str = ''
    end = 'DEKUJEME ZA VYUZITI NASEHO SYSTEMU'
    for lst in cont_to_format:
        for pair in lst:
            cont_str = cont_str + row_to_format.format(*pair) + '\n'
        cont_str = cont_str + 45*'='+ '\n'

    return beg + cont_str + end

#listofkeys = ['znacka', 'model', 'rv', {'tech': ['vykon', 'spotreba', 'palivo', 'prevodovka']}, 'kategorie', 'cena']
db = readDB('not_rented.txt')

options = ['HLEDAT', 'PUJCIT', 'KONEC']

while True:
    print('VITEJTE V NASI CAR RENTAL COMPANY')
    print('MATE NA VYBER, HLEDAT, PUJCIT, KONEC')
    vyber = input('ZADEJ VOLBU: ').upper()
    if vyber == options[0]:
        comp_items = ['POLOŽKA', 'HODNOTA', 'ZNAMENKO']
        tuples = []
        while True:
            tup = ()
            inp = 0
            print('Vyhledavani v nasi databazi.\nZadej v jake kategorii hledas co a potom znamenko porovnavani')
            for item in comp_items:
                inp = [input('Zadej ' + item + ' :\n')]
                if inp == ['']:
                    break
                tup = tup + tuple(inp)
                print('tup',tup)
            tuples.append(tup)
            if inp == ['']:
                break
        s_result = getMore(db, tuples)
        print(printResult(s_result,db))

    elif vyber == options[1]:
        print('Rozhodli jste si půjčit auto, skvělé!')
        rent_id = input('Zadejte ID auta prosím: ')
        if rentCar(int(rent_id), 'rented.txt','not_rented.txt'):
            print('Gratulujeme! Máte zarezervované auto číslo', rent_id)
        pass

    elif vyber == options[2]:
        print('KONEC')
        break
    else:
        print('Chybna volba')
