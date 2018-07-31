def readfile(filename):
    s = open(filename)
    content = s.read()
    s.close()
    return content


def writetofile(content, filename, mode):
    s = open(filename, mode)
    for item in content:
        s.write(item)
    s.close()


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


def encode(dictionary):
    encoded = []

    for key, value in dictionary.items():
        if type(value) == type({}):
            encoded.append(str(key) + '=')
            for lkey, lvalue in value:
                encoded.append(str(lkey) + '=' + str(lvalue))
        else:
            encoded.append(str(key) + '=' + str(value))

    return encoded


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


def addtoDBfile(data, db_file):
    writetofile(encode(data), db_file, 'a')


def updateDBfile(db, db_file):
    writetofile(encode(db), db_file, 'w')


def createItem(list_of_keys):
    newitem = {}
    for key in list_of_keys:

        if type(key) == type({}):
            newitem.update({list(key.keys())[0]: {}})

            # ERROR MESSAGE
            if len(key.keys()) > 1:
                print('Too many subkeys on one keylist position: {}'.format(list(key.keys())[0]))
                return {}

            for lkey in list(key.values())[0]:
                print(lkey)
                newitem[list(key.keys())[0]].update({lkey: input('Insert value for {} subcategory in {} category'.format(lkey, list(key.keys())[0]))})

        else:
            newitem.update({key: input('Insert value for {} category'.format(key))})

    return newitem


listofkeys = ['znacka', 'model', 'rv', {'tech': ['vykon', 'spotreba', 'palivo', 'prevodovka']},'kategorie','cena']
print(createItem(listofkeys))
db = readDB('sample_database_availible.txt')
print(len(db.keys()))
