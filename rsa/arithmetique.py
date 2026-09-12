import random
from math import log2
#rsa
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
    if d!=1:
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

def generer_cles(bits):
    p=generer_premier(bits)
    q=generer_premier(bits)
    d=None
    while p==q:
        p=generer_premier(bits)
    n=p*q
    phi=(p-1)*(q-1)
    e=random.randint(2,phi-1)
    while d==None:  
        e=random.randint(2,phi-1)
        d=inverse_modulaire(e,phi)
    return ((n,e),(n,d))

def chiffrement(m,cle_publique):
    n,e=cle_publique
    return exponentiation_rapide(m,e,n)

def dechiffrement(M,cle_prive):
    n,d=cle_prive
    return exponentiation_rapide(M,d,n)


#attaque
def factoriser(n):
    if n%2==0:
        return 2
    if n==0 or n==1:return False
    i=3
    while i*i<=n:
        if n%i==0:
            return i
        i+=2
    return None


#critère de réussite
from math import isqrt

for n in range(2, 20000):
    f = factoriser(n)
    if f is None:
        assert est_premier(n, 20), ("dit premier a tort", n)
    else:
        assert n % f == 0 and est_premier(f, 20), ("mauvais facteur", n, f)
        assert all(n % k != 0 for k in range(2, f)), ("pas le plus petit", n, f)
print("OK")

for bits in [16, 20, 24]:
    (n, e), _ = generer_cles(bits)
    p = factoriser(n)
    assert p is not None and n % p == 0
    print(bits, "bits :", n, "=", p, "x", n//p)

import time
for bits in [12, 16, 20, 24, 28, 32]:
    (n, e), _ = generer_cles(bits)
    t = time.time(); factoriser(n); dt = time.time()-t
    print("%2d bits par premier | n = %3d bits | %.4f s" % (bits, n.bit_length(), dt))