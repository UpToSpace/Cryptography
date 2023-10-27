import random
# import Crypto.Util.number


def generate_rsa_prs(t):
    seq = ''

    # Генерация двух 256-разрядных простых чисел
    p = 100148503798148397260882949024782135675088928894197678172480871597365270535129
    q = 11198040523770520961764683848152092110827665974402165189171445670862344238922

    print("\np: ", p)
    print("q: ", q)

    # Вычисление произведения p и q
    n = p * q
    print("n: ", n)

    # Выбор открытого ключа e
    phi = (p - 1) * (q - 1)
    e = generate_coprime(phi)
    print("e: ", e)

    x0 = random.randint(0, n - 1)
    print("x0: ", x0)

    x_t = pow(x0, e, n)

    for i in range(t):
        x_t = pow(x_t, e, n)
        seq += str(x_t % 2)
    return seq


def extended_gcd(a, b): # расширенный алгоритм евклида
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def generate_coprime(phi):
    while True:
        e = random.randrange(2, phi)
        gcd, x, y = extended_gcd(e, phi)
        if gcd == 1:
            return e