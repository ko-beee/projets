import random
from math import log2

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

def exponentiation_rapide(a,b,n):
    p=1%n
    s=a%n
    while b>0:
        if b%2==1:
            p=p*s%n
        b=b//2
        s=s**2%n
    return p
            
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

def est_premier(p,k):
    if p==2:
        return True
    g=p-1
    s=0
    while g%2==0 :
        g=g//2
        s+=1
    for i in range (k):
        a=random.randint(2, p)
        while a%p ==0:
            a=random.randint(2, p)
        d=exponentiation_rapide(a,g,p)
        for c in range (s):
            d2=exponentiation_rapide(d,2,p)
            if d!=1 and d!=p-1:
                if d2==1:
                    return False
            d=d2
        if d!=1:
            return False
    return True

def generer_premier(bits):
    b=False
    while b==False:
        a=random.randint(2**(bits-1),2**bits-1)
        if a%2==0: b=False
        else:
            b=est_premier(a,20)
    return a




#critère de réussite
import random, time


import random, time

def oracle(p, k=40):
    """Vérificateur de test uniquement. pow natif autorisé ici, jamais dans le code."""
    if p < 2:
        return False
    for _ in range(k):
        a = random.randrange(2, p - 1)
        if pow(a, p - 1, p) != 1:
            return False
    return True



for bits in [8, 16, 32, 64, 128, 256, 512]:
    t = time.time()
    for _ in range(20):
        p = generer_premier(bits)
        assert oracle(p), ("pas premier", bits, p)
        assert p.bit_length() == bits, ("mauvaise taille", bits, p.bit_length())
    print("%4d bits : OK   20 premiers en %.2f s" % (bits, time.time() - t))

ech = {generer_premier(32) for _ in range(50)}
print("valeurs distinctes sur 50 tirages :", len(ech))

# nombre de candidats testés avant succès, à comparer à ton estimation par ln
essais = []
for _ in range(20):
    n = 0
    while True:
        n += 1
        c = random.randrange(2**511, 2**512) | 1
        if est_premier(c, 20):
            break
    essais.append(n)
print("candidats impairs testés à 512 bits : moyenne %.0f sur 20 tirages" % (sum(essais)/len(essais)))

for _ in range(2000):
    a, b, n = random.randrange(0,10**4), random.randrange(0,10**4), random.randrange(1,10**4)
    assert exponentiation_rapide(a,b,n) == pow(a,b,n), (a,b,n)

for n in range(1,60):
    for a in range(0,60):
        for b in range(0,40):
            assert exponentiation_rapide(a,b,n) == pow(a,b,n), (a,b,n)

p = 2**200-1
for nom, f in [("gloutonne", exponentiation_modulaire), ("binaire", exponentiation_rapide)]:
    t=time.time(); f(3, p-1, p); print(nom, "%.4f s" % (time.time()-t))
print("OK")