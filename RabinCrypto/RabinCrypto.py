import sys

#config p [0] and q [1] both === 3 mod 4
private = [67317488495423799828622848507978495932353996728161028786981841987819294308223,
           88916115075035204878391459198246505521471227845052526477778284545394011218787]

private = [277,
           331]

#calc n
public = private[0]*private[1]
print(public)

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

msg = "Testowa wiadomosc"

msg_dec = int.from_bytes(msg.encode(), sys.byteorder)
msg_dec = 40569

print("Wiadomosc")
print(msg_dec)
print("---------")

encrypted = pow(msg_dec, 2, public)

print("Szyfrogram")
print(encrypted)
print("---------")

#chiñskie twierdzenie o resztach

_, a, b = egcd(private[0], private[1])

r = pow(encrypted, int((private[0]+1)/4), private[0])
s = pow(encrypted, int((private[1]+1)/4), private[1])
x = (a*private[0]*s + b*private[1]*r) % public
y = (a*private[0]*s - b*private[1]*r) % public


dM1 = x
dM2 = y
dM3 = -x % public
dM4 = -y % public


print(dM1)
print(dM2)
print(dM3)
print(dM4)

