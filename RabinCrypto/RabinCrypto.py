import sys

#config p [0] and q [1] both === 3 mod 4
private = [67317488495423799828622848507978495932353996728161028786981841987819294308223,
           88916115075035204878391459198246505521471227845052526477778284545394011218787]

#private = [167,
 #          151]

#calc n
public = private[0]*private[1]
print(public)

def egcd(x, y):
    xp, xq = 1, 0
    yp, yq = 0, 1
    while y:
        q = int(x / y)
        t, tp, tq = x, xp, xq
        x, xp, xq = y, yp, yq
        y, yp, yq = t - q * x, tp - q * xp, tq - q * xq
    return (x, xp, xq)


msg = "Testowa wiadomosc"

msg_dec = int.from_bytes(msg.encode(), sys.byteorder)
msg_dec = 2216014906335081603549288532914445221681335498308087915761920903129755171763383337516126256589945957688750848529770360764804066357509839523612945675889149

print("Wiadomosc")
print(msg_dec)
print("---------")

encrypted = pow(msg_dec, 2, public)

print("Szyfrogram")
print(encrypted)
print("---------")

#chinskie twierdzenie o resztach
'''
_, a, b = egcd(private[0], private[1])

r = pow(encrypted, int((private[0]+1)/4), private[0])
r1 = (encrypted**int(private[0]+1/4)) % private[0]
s = pow(encrypted, int((private[1]+1)/4), private[1])
x = (a*private[0]*s + b*private[1]*r) % public
y = (a*private[0]*s - b*private[1]*r) % public

print(r)
print(r1)

dM1 = x
dM2 = y
dM3 = -x % public
dM4 = -y % public


print(dM1)
print(dM2)
print(dM3)
print(dM4)
'''

m1 = pow(encrypted, int((private[0]+1)/4), private[0])
m2 = private[0] - pow(encrypted, int((private[0]+1)/4), private[0])
m3 = pow(encrypted, int((private[1]+1)/4), private[1])
m4 = private[1] - pow(encrypted, int((private[1]+1)/4), private[1])

_, aE, bE = egcd(private[0], private[1])

a = private[1]*bE
b = private[0]*aE

dM1 = pow((a*m1 + b*m3), 1, public)
dM2 = pow((a*m1 + b*m4), 1, public)
dM3 = pow((a*m2 + b*m3), 1, public)
dM4 = pow((a*m2 + b*m4), 1, public)

print(dM1)
print(dM2)
print(dM3)
print(dM4)

