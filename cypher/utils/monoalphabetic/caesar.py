def decrypt_once(ciphertext, shift):
    result = ''

    for sym in ciphertext:
        if sym.isupper():  # check if it's an uppercase character
            # shift to left by `shift` positions to get its original value
            result += chr((ord(sym) - shift - ord('A')) % 26 + ord('A'))
        elif sym.islower():  # check if it's an lowercase character
            result += chr((ord(sym) - shift - ord('a')) % 26 + ord('a'))
        elif sym.isdigit():  # check if it's a number
            # shift actual value of number
            result += str((int(sym) - shift) % 10)
        else:
            # if its neither alphabetical nor a number - just leave it
            result += sym
    return result


def encrypt_caesar(plaintext, shift):
    result = ''

    for sym in plaintext:
        if sym.isupper():  # check if it's an uppercase character
            # shift the current character by `shift` position
            result += chr((ord(sym) + shift - ord('A')) % 26 + ord('A'))
        elif sym.islower():  # check if it's an lowercase character
            result += chr((ord(sym) + shift - ord('a')) % 26 + ord('a'))
        elif sym.isdigit():  # check if it's a number
            # shift actual value of number
            result += str((int(sym) + shift) % 10)
        else:
            # if its neither alphabetical nor a number - just leave it
            result += sym
    return result


def decrypt_caesar(ciphertext, shift=0):
    if shift:
        return decrypt_once(ciphertext, shift)
    else:
        return [decrypt_once(ciphertext, shift) for shift in range(26)]
