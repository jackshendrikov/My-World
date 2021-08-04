def solve_atbash(text):
    result = ''

    for sym in text:
        if sym.isupper():
            # character is mapped to its reverse in the alphabet
            result += chr(ord('Z') + ord('A') - ord(sym))
        elif sym.islower():
            result += chr(ord('z') + ord('a') - ord(sym))
        elif sym.isdigit():
            result += str(10 - int(sym))
        else:
            result += sym

    return result
