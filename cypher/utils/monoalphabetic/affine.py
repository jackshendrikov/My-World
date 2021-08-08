# Extended  Euclidean Algorithm for finding modular inverse
def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y


def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


def encrypt_affine(plaintext, key):
    # C = (a*P + b) % 26
    result = ''
    for sym in plaintext:
        if sym.isalpha():
            if sym.isupper(): a_sym = ord('A')
            else: a_sym = ord('a')

            result += chr(((key[0] * (ord(sym) - a_sym) + key[1]) % 26) + a_sym)
        else:
            result += sym

    return result


def decrypt_affine(ciphertext, key):
    # P = (a^-1 * (C - b)) % 26
    result = ''

    for sym in ciphertext:
        if sym.isalpha():
            if sym.isupper(): a_sym = ord('A')
            else: a_sym = ord('a')

            result += chr(((modinv(key[0], 26) * (ord(sym) - a_sym - key[1])) % 26) + a_sym)
        else:
            result += sym

    return result
