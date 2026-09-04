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
        return 1%n
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

def inverse_modulaire(a, n):
    """Renvoie l'inverse de a modulo n, ou None s'il n'existe pas."""
    d,u,v=euclide_etendu(a,n)
    if d**2!=1:
        return None
    else:
        return u%n



#critère de réussite

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

for _ in range(1000):
    n = random.randint(2, 10**6)
    a = random.randint(1, n-1)
    inv = inverse_modulaire(a, n)
    if math.gcd(a, n) == 1:
        assert inv is not None, f"inverse manquant : a={a} n={n}"
        assert (a * inv) % n == 1, f"inverse faux : a={a} n={n} → {inv}"
    else:
        assert inv is None, f"inverse impossible non détecté : a={a} n={n}"

from math import gcd
from random import randrange

for _ in range(5000):
    a, n = randrange(0, 10**6), randrange(2, 10**6)
    assert exponentiation_modulaire(a, 0, n) == 1 % n, (a, n)
    x = inverse_modulaire(a, n)
    if gcd(a, n) == 1:
        assert x is not None and 0 <= x < n and (a * x) % n == 1, (a, n, x)
    else:
        assert x is None, (a, n, x)

for n in range(2, 60):          # balayage exhaustif des petits cas
    for a in range(0, 60):
        x = inverse_modulaire(a, n)
        assert (x is None) == (gcd(a, n) != 1), (a, n, x)
        if x is not None:
            assert 0 <= x < n and (a * x) % n == 1, (a, n, x)

print("OK")

for n in range(1, 60):
    for a in range(0, 60):
        assert exponentiation_modulaire(a, 0, n) == 1 % n, (a, n)
print("OK")