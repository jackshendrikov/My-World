"""
a   AAAAA   g     AABBA   n    ABBAA   t     BAABA
b   AAAAB   h     AABBB   o    ABBAB   u-v   BAABB
c   AAABA   i-j   ABAAA   p    ABBBA   w     BABAA
d   AAABB   k     ABAAB   q    ABBBB   x     BABAB
e   AABAA   l     ABABA   r    BAAAA   y     BABBA
f   AABAB   m     ABABB   s    BAAAB   z     BABBB
"""
import re


def generate_dict(original_table=True):
    bacon_dict = {}

    for letter_num in range(26):
        letter = chr(65 + letter_num)

        if original_table:
            # 21 means letter `V`, 9 -> `J`, since we have repetitions (i=j, u=v) - we need to shift our letters by 1
            # (when letter_num >= 9) to `J` have an identical code to `I`, and now since we have a repetition we have
            # to shift all the letters further so that they don't overwrite each other;
            #
            # Next we need to shift our letters by 2 (when letter_num >= 21, `2` means we taking into account the
            # previous shift) to `V` have an identical code to `U`, and now since we have 2 repetitions we have to
            # shift all the letters further by 2 so that they also don't overwrite each other;
            if letter_num >= 21:
                letter_num -= 2
                letter = chr(65 + letter_num + 2)
            elif letter_num >= 9:
                letter_num -= 1  # we do that in order to get the same representation for `J` as for `I`
                letter = chr(65 + letter_num + 1)  # now we do +1 to get char `J`, not `I`; as a result, for letter
                # `J` we have representation of `I`

        tmp = bin(letter_num)[2:].zfill(5)
        tmp = tmp.replace('0', 'A')
        tmp = tmp.replace('1', 'B')
        bacon_dict[letter] = tmp

    return bacon_dict


def decrypt_bacon(ciphertext, original=True):
    bacon_dict = generate_dict(original_table=original)
    ciphertext = re.sub(r'[^AB]+', '', ciphertext)
    split_ciphertext = [ciphertext[i:i+5] for i in range(0, len(ciphertext), 5)]
    result = ''

    for cryptogram in split_ciphertext:
        try:
            result += list(bacon_dict.keys())[list(bacon_dict.values()).index(cryptogram)]  # get dict key by value
        except ValueError:
            result += '?'

    return result


def encrypt_bacon(plaintext, original=True):
    bacon_dict = generate_dict(original_table=original)
    result = ''

    for sym in plaintext:
        if sym.isupper():
            result += bacon_dict.get(sym)
        elif sym.islower():
            result += bacon_dict.get(sym.upper())

    return result

