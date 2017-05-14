import sys
import getopt
from KeyGen import KeyGen

#config p [0] and q [1] both === 3 mod 4
private = []

#private = [7,11]
countedBytes = 32
countedCheckSumBits = 64

#calc n
public = 0

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
    p = ((private[0] + 1) // 4, (private[1] + 1) // 4)

    m = (pow(encrypted, p[0], private[0]), private[0] - pow(encrypted, p[0], private[0]),
        pow(encrypted, p[1], private[1]), private[1] - pow(encrypted, p[1], private[1]))

    modInv = egcd(private[0], private[1])

    a = private[1] * modInv[1]
    b = private[0] * modInv[0]

    M = (pow((a * m[0] + b * m[2]), 1, public), pow((a * m[0] + b * m[3]), 1, public),
        pow((a * m[1] + b * m[2]), 1, public), pow((a * m[1] + b * m[3]), 1, public))

    return M


def encrypt_file(fromFile, toFile):
    fileWrite = open(toFile, "wb")
    with open(fromFile, "rb") as fread:
        fbytes = fread.read(countedBytes)
        while fbytes:
            enc_msg = encrypt(encode(fbytes))
            fileWrite.write(enc_msg.to_bytes((public.bit_length() + 7) // 8, sys.byteorder))
            fbytes = fread.read(countedBytes)
    fileWrite.close()


def decrypt_file(fromFile, toFile):
    fileWrite = open(toFile, "wb")
    with open(fromFile, "rb") as fread:
        fbytes = fread.read(countedBytes * 2)
        while fbytes:
            fbytes = int.from_bytes(fbytes, sys.byteorder)
            dec_msg = decode(decrypt(fbytes))
            fileWrite.write(dec_msg.to_bytes(countedBytes, sys.byteorder))
            fbytes = fread.read(countedBytes * 2)
    fileWrite.close()
        


def main(argv):

    method = ''
    fromFile = ''
    toFile = ''
    
    try:
        opts, args = getopt.getopt(argv, "hedkf:t:", ["help", "encrypt", "decyrypt", "keygen" "fromfile=", "tofile="])
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
        elif opt in ("-k", "--keygen"):
            method = "key"
        elif opt in ("-f", "--fromfile"):
            fromFile = arg
        elif opt in ("-t", "--tofile"):
            toFile = arg
        else:
            assert False, "Error"

    if method == 'enc':
        
        global public
        fileRead = open("keys/pubkey.txt", "r")
        public = int(fileRead.readline().strip())
        fileRead.close()
        
        encrypt_file(fromFile, toFile)
    elif method == 'dec':
        
        global private

        fileRead = open("keys/privkeys.txt", "r")
        private.append(int(fileRead.readline().strip()))
        private.append(int(fileRead.readline().strip()))
        fileRead.close()
        
        public = private[0] * private[1]

        decrypt_file(fromFile, toFile)
    elif method == 'key':
        keygen = KeyGen()
        privKeys = keygen.keyGen(countedBytes*8)
        pubKey = privKeys[0] * privKeys[1]
        fileWrite = open("keys/privkeys.txt", "w")
        fileWrite.write('\n'.join((str(privKeys[0]), str(privKeys[1]))))
        fileWrite.close()

        fileWrite = open("keys/pubkey.txt", "w")
        fileWrite.write(str(pubKey))
        fileWrite.close()


def help():
    print("Usage: ./RabinCrypto OPTION [VALUE]")
    print("Options:")
    print("     -h --help")
    print("     -e --encrypt")
    print("     -d --decrypt")
    print("     -k --keygen")
    print("     -f --fromfile")
    print("     -t --tofile")

if __name__ == "__main__":
    main(sys.argv[1:])    