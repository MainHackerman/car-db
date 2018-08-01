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


listofkeys = ['znacka', 'model', 'rv', {'tech': ['vykon', 'spotreba', 'palivo', 'prevodovka']}, 'kategorie', 'cena']
db = readDB('not_rented.txt')
print(len(db.keys()))
print(db)
skoda = getCar('vykon', '76', '>=', db)
print(skoda)
