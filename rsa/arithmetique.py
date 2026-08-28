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

if __name__ == "__main__":
    import random
    import math
    for _ in range(1000):
        a = random.randint(2, 10**6)
        b = random.randint(2, 10**6)
        n = random.randint(2, 10**6)
        assert exponentiation_modulaire(a, b, n) == pow(a, b, n)
    print("1000 tests passés")