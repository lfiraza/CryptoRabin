import sys

#config p [0] and q [1] both === 3 mod 4
private = [67317488495423799828622848507978495932353996728161028786981841987819294308223,
           88916115075035204878391459198246505521471227845052526477778284545394011218787]


#private = [7,11]

#calc n
public = private[0]*private[1]
#print("Klucz publiczny")
#print(public)
#print("----------")

def egcd(x, y):
    xp, xq = 1, 0
    yp, yq = 0, 1
    while y:
        q = x // y
        t, tp, tq = x, xp, xq
        x, xp, xq = y, yp, yq
        y, yp, yq = t - q * x, tp - q * xp, tq - q * xq
    return (xp, xq)


msg = 134354432543243524353223466365

encrypted = pow(msg, 2, public)


#chinskie twierdzenie o resztach
p = ((private[0]+1)//4, (private[1]+1)//4)



m = (pow(encrypted, p[0], private[0]), private[0] - pow(encrypted, p[0], private[0]),
    pow(encrypted, p[1], private[1]), private[1] - pow(encrypted, p[1], private[1]))

modInv = egcd(private[0], private[1])

a = private[1]*modInv[1]
b = private[0]*modInv[0]



M = (pow((a*m[0] + b*m[2]), 1, public), pow((a*m[0] + b*m[3]), 1, public),
     pow((a*m[1] + b*m[2]), 1, public), pow((a*m[1] + b*m[3]), 1, public))

print(M)

