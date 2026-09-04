def exponentiation_modulaire(a, b, n):
    """Renvoie a^b mod n."""
    i=0
    f=0
    c=[a]
    j=[1]
    while j[f]<b:
        for l in range (len(j)):
            if (j[i-l]+j[i])<=b:
                c.append(c[i]*c[i-l])
                c[i+1]%=n
                j.append(j[i-l]+j[i])
                i+=1
                f+=1
    if b==0:
        return 1
    return c[i]%n

def euclide_etendu(a, b):
    #Renvoie (d, u, v) tels que d = pgcd(a, b) et a*u + b*v = d.
    u2=1
    u1=0
    v2=0
    v1=1
    while b!=0:
        q=a // b
        a,b = b, a%b
        v1,v2 = v2-v1*q, v1
        u1,u2 = u2-u1*q, u1
    d=a
    return (d,u2,v2)

import math, random

for _ in range(1000):
    a = random.randint(2, 10**6)
    b = random.randint(2, 10**6)
    n = random.randint(2, 10**6)
    assert exponentiation_modulaire(a, b, n) == pow(a, b, n)

for _ in range(1000):
    a = random.randint(1, 10**6)
    b = random.randint(1, 10**6)
    d, u, v = euclide_etendu(a, b)
    assert d == math.gcd(a, b), f"pgcd faux : a={a} b={b} → {d}"
    assert a*u + b*v == d,      f"Bézout faux : a={a} b={b} → u={u} v={v}"
