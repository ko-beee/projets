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
        d=exponentiation_modulaire(a,g,p)
        for c in range (s):
            d2=exponentiation_modulaire(d,2,p)
            if d!=1 and d!=p-1:
                if d2==1:
                    return False
            d=d2
        if d!=1:
            return False
    return True




#critère de réussite

import math, random


def crible(n):
    est = [True]*(n+1); est[0]=est[1]=False
    for i in range(2, int(n**0.5)+1):
        if est[i]:
            for m in range(i*i, n+1, i): est[m] = False
    return est

VRAI = crible(50000)
CARMICHAEL = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585,
              15841, 29341, 41041, 46657, 1042789205881, 1396066334401]

fn = [p for p in range(3, 50000) if VRAI[p] and not est_premier(p, 20)]
fp = [p for p in range(3, 50000) if not VRAI[p] and est_premier(p, 20)]
print("faux negatifs :", len(fn), fn[:5])
print("faux positifs :", len(fp), fp[:5])

for c in CARMICHAEL:
    r = sum(est_premier(c, 20) for _ in range(100))
    print(c, "declare premier", r, "/100")

