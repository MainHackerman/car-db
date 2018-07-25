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
                print('TRUE')
                polozky = pair.split('=')
                print(polozky[0][4:])
                decoded[dictionary].update({polozky[0][4:]: polozky[1]})
            else:
                polozky = pair.split('=')
                decoded[polozky[0]] = polozky[1]
                dictionary = {}

    return decoded


def encode(dictionary, filename):
    encoded = []

    for key, value in dictionary.items():
        if type(value) == type({}):
            encoded.append(str(key) + '=')
            for lkey, lvalue in value:
                encoded.append(str(lkey) + '=' + str(lvalue))
        else:
            encoded.append(str(key) + '=' + str(value))

    return encoded

print(decode('databaze.txt'))
