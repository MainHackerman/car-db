def readfile(filename):
    s = open(filename)
    content = s.read()
    s.close()
    return content

def decode(filename):
    decoded = {}
    raw = readfile(filename)
    rows = raw.split('\n')
    prev_pair=''
    dictionary={}
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
                dictionary={}
            prev_pair = pair

    return decoded

print(decode('databaze.txt'))