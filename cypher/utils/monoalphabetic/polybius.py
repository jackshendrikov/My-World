def encrypt_polybius(plaintext, key):
    keys_list = list(key)
    result = ''

    for sym in plaintext.upper():
        if sym.isalnum():
            try:
                sym_index = keys_list.index(sym)

                # get the index of an element (row, column) as if it were a matrix (5x5)
                result += str(sym_index // 5 + 1) + str(sym_index % 5 + 1)
            except ValueError:
                return False

    return result


def decrypt_polybius(ciphertext, key):
    keys_list = list(key)
    result = ''

    for i in range(0, len(ciphertext), 2):
        x = int(ciphertext[i]) - 1
        y = int(ciphertext[i + 1]) - 1

        # get letter by index
        result += keys_list[x*5 + y]

    return result
