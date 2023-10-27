from math import sqrt


def get_gcd2(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b


def get_gcd3(a, b, c):
    return get_gcd2(get_gcd2(a, b), c)


def get_prime(min, max): #найти простые числа
    sieve = []
    a = [0] * (max + 1)

    for i in range(max + 1):
        a[i] = 1

    for i in range(2, int(sqrt(max)) + 1):
        if a[i] == 1:
            j = 2
            while i * j <= max:
                a[i * j] = 0
                j = j + 1

    for i in range(2, max + 1):
        if a[i] == 1:
            # print(i, end = ' ')
            sieve.append(i)

    sieve = list(filter(lambda num: num >= min, sieve))
    return (sieve)


def get_factors(n): #найти простые множители
    result = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            result.append(d)
            n //= d
        else:
            d += 1
    if n > 1:
        result.append(n)
    canon = str(n) + ' = ' + str(result[0])
    for i in range(1, len(result)):
        canon += ' * ' + str(result[i])
    return canon


def is_prime(n): #простое ли число
    k = 0
    for i in range(2, n // 2 + 1):
        if (n % i == 0):
            k = k + 1
    if k <= 0:
        return True
    else:
        return False