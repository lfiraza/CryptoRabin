import sys

#config p [0] and q [1] both === 3 mod 4
private = [67317488495423799828622848507978495932353996728161028786981841987819294308223,
           88916115075035204878391459198246505521471227845052526477778284545394011218787]

private = [7,11]

#calc n
public = private[0]*private[1]
print("Klucz publiczny")
print(public)
print("----------")

def egcd(x, y):
    xp, xq = 1, 0
    yp, yq = 0, 1
    while y:
        q = int(x / y)
        t, tp, tq = x, xp, xq
        x, xp, xq = y, yp, yq
        y, yp, yq = t - q * x, tp - q * xp, tq - q * xq
    return (xp, xq)


msg = 45

print("Wiadomosc")
print(msg_dec)
print("---------")

encrypted = pow(msg, 2, public)

print("Szyfrogram")
print(encrypted)
print("---------")

#chinskie twierdzenie o resztach

m1 = pow(encrypted, int((private[0]+1)/4), private[0])
m2 = private[0] - pow(encrypted, int((private[0]+1)/4), private[0])
m3 = pow(encrypted, int((private[1]+1)/4), private[1])
m4 = private[1] - pow(encrypted, int((private[1]+1)/4), private[1])

modInv = egcd(private[0], private[1])

a = private[1]*modInv[1]
b = private[0]*modInv[0]

M1 = pow((a*m1 + b*m3), 1, public)
M2 = pow((a*m1 + b*m4), 1, public)
M3 = pow((a*m2 + b*m3), 1, public)
M4 = pow((a*m2 + b*m4), 1, public)

print(M1)
print(M2)
print(M3)
print(M4)

