import sys, getopt

#config p [0] and q [1] both === 3 mod 4
private = [67317488495423799828622848507978495932353996728161028786981841987819294308223,
           88916115075035204878391459198246505521471227845052526477778284545394011218787]

#private = [7,11]

countedBytes = 32
countedCheckSumBits = 64

#calc n
public = private[0]*private[1]

def hexString(bits):
    listF = ['f'] * (bits // 4)
    return ''.join(listF)

bitsForControlSum = int(hexString(countedCheckSumBits), 16)

def encode(msgBytes):
    fbytes = int.from_bytes(msgBytes, sys.byteorder)
    bytesPlus = fbytes << countedCheckSumBits
    controlSum = fbytes & bitsForControlSum
    fbytes = bytesPlus | controlSum
    return fbytes

def decode(M):
    for fbytes in M:
        controlSum = (fbytes >> countedCheckSumBits) & bitsForControlSum
        checkerSum = fbytes & bitsForControlSum
        if checkerSum == controlSum:
            return fbytes >> countedCheckSumBits
    return False
        

def egcd(x, y):
    xp, xq = 1, 0
    yp, yq = 0, 1
    while y:
        q = x // y
        t, tp, tq = x, xp, xq
        x, xp, xq = y, yp, yq
        y, yp, yq = t - q * x, tp - q * xp, tq - q * xq
    return (xp, xq)


def encrypt(msg):
    return pow(msg, 2, public)

def decrypt(encrypted):
    #chinskie twierdzenie o resztach
    p = ((private[0]+1)//4, (private[1]+1)//4)

    m = (pow(encrypted, p[0], private[0]), private[0] - pow(encrypted, p[0], private[0]),
        pow(encrypted, p[1], private[1]), private[1] - pow(encrypted, p[1], private[1]))

    modInv = egcd(private[0], private[1])

    a = private[1]*modInv[1]
    b = private[0]*modInv[0]

    M = (pow((a*m[0] + b*m[2]), 1, public), pow((a*m[0] + b*m[3]), 1, public),
        pow((a*m[1] + b*m[2]), 1, public), pow((a*m[1] + b*m[3]), 1, public))

    return M


def encrypt_file(fromFile, toFile):
    fileWrite = open(toFile, "wb")
    with open(fromFile, "rb") as fread:
        fbytes = fread.read(countedBytes)
        while fbytes:
            enc_msg = encrypt(encode(fbytes))
            fileWrite.write(enc_msg.to_bytes((enc_msg.bit_length() + 7) // 8, sys.byteorder))
            fbytes = fread.read(countedBytes)
    fileWrite.close()


def decrypt_file(fromFile, toFile):
    fileWrite = open(toFile, "wb")
    with open(fromFile, "rb") as fread:
        fbytes = fread.read(countedBytes*2)
        while fbytes:
            fbytes = int.from_bytes(fbytes, sys.byteorder)
            dec_msg = decode(decrypt(fbytes))
            fileWrite.write(dec_msg.to_bytes((dec_msg.bit_length() + 7) // 8, sys.byteorder))
            fbytes = fread.read(countedBytes*2)
    fileWrite.close()
        


def main(argv):

    method = ''
    fromFile = ''
    toFile = ''
    
    try:
        opts, args = getopt.getopt(argv, "hedf:t:", ["help", "encrypt", "decyrypt", "fromfile=", "tofile="])
    except getopt.GetoptError as error:
        print(error)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
        elif opt in ("-d", "--decrypt"):
            method = "dec"
        elif opt in ("-e", "--encrypt"):
            method = "enc"
        elif opt in ("-f", "--fromfile"):
            fromFile = arg
        elif opt in ("-t", "--tofile"):
            toFile = arg
        else:
            assert False, "Error"

    if method == 'enc':
        encrypt_file(fromFile, toFile)
    elif method == 'dec':
        decrypt_file(fromFile, toFile)

def help():
    print("Usage: ./RabinCrypto OPTION [VALUE]")
    print("Options:")
    print("     -h --help")
    print("     -e --encrypt")
    print("     -d --decrypt")
    print("     -f --fromfile")
    print("     -t --tofile")

if __name__ == "__main__":
    main(sys.argv[1:])    