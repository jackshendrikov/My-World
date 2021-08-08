from django.shortcuts import render
from .utils.monoalphabetic.atbash import solve_atbash
from .utils.monoalphabetic.bacon import encrypt_bacon, decrypt_bacon
from .utils.monoalphabetic.caesar import encrypt_caesar, decrypt_caesar
from .utils.monoalphabetic.polybius import encrypt_polybius, decrypt_polybius
from .utils.monoalphabetic.affine import encrypt_affine, decrypt_affine


def cypher_main(request):
    return render(request, 'cypher/main.html')


def caesar(request):
    if request.method == 'POST':
        caesarList = False
        decrypt = False

        if request.POST['cipherEncrypt'] == 'False':
            decrypt = True
            ciphertext = request.POST['ciphertext']
            shift = request.POST.get('shift', False)

            if shift:
                shift = int(shift)
                plaintext = decrypt_caesar(ciphertext, shift=shift)
            else:
                caesarList = True
                plaintext = decrypt_caesar(ciphertext)
        else:
            plaintext = request.POST['plaintext']
            shift = int(request.POST['shift'])
            ciphertext = encrypt_caesar(plaintext, shift)

        return render(request, 'cypher/caesar.html', {'plaintext': plaintext, 'shift': shift,
                                                      'ciphertext': ciphertext, 'caesarList': caesarList,
                                                      'decrypt': decrypt})

    return render(request, 'cypher/caesar.html')


def atbash(request):
    if request.method == 'POST':
        decrypt = False

        if request.POST['cipherEncrypt'] == 'False':
            decrypt = True

            ciphertext = request.POST['ciphertext']
            plaintext = solve_atbash(ciphertext)
        else:
            plaintext = request.POST['plaintext']
            ciphertext = solve_atbash(plaintext)

        return render(request, 'cypher/atbash.html', {'plaintext': plaintext, 'ciphertext': ciphertext,
                                                      'decrypt': decrypt})

    return render(request, 'cypher/atbash.html')


def rot13(request):
    if request.method == 'POST':
        decrypt = False

        if request.POST['cipherEncrypt'] == 'False':
            decrypt = True

            ciphertext = request.POST['ciphertext']
            plaintext = decrypt_caesar(ciphertext, shift=13)
        else:
            plaintext = request.POST['plaintext']
            ciphertext = encrypt_caesar(plaintext, shift=13)

        return render(request, 'cypher/rot13.html', {'plaintext': plaintext, 'ciphertext': ciphertext,
                                                     'decrypt': decrypt})

    return render(request, 'cypher/rot13.html')


def bacon(request):
    if request.method == 'POST':
        decrypt = False
        origin_table = request.POST.get('originalTable', False)

        if request.POST['cipherEncrypt'] == 'False':
            decrypt = True
            ciphertext = request.POST['ciphertext']

            if origin_table:
                plaintext = decrypt_bacon(ciphertext)
            else:
                plaintext = decrypt_bacon(ciphertext, original=False)
        else:
            plaintext = request.POST['plaintext']

            if origin_table:
                ciphertext = encrypt_bacon(plaintext)
            else:
                ciphertext = encrypt_bacon(plaintext, original=False)

        return render(request, 'cypher/bacon.html', {'plaintext': plaintext, 'ciphertext': ciphertext,
                                                     'decrypt': decrypt, 'originTable': origin_table})

    return render(request, 'cypher/bacon.html')


def polybius(request):
    if request.method == 'POST':
        decrypt = False
        encryption_key = request.POST['encryptionKey']

        if request.POST['cipherEncrypt'] == 'False':
            decrypt = True
            ciphertext = request.POST['ciphertext']
            plaintext = decrypt_polybius(ciphertext, encryption_key)
        else:
            plaintext = request.POST['plaintext']
            ciphertext = encrypt_polybius(plaintext, encryption_key)

        return render(request, 'cypher/polybius.html', {'plaintext': plaintext, 'ciphertext': ciphertext,
                                                        'decrypt': decrypt, 'encryption_key': encryption_key})

    return render(request, 'cypher/polybius.html')


def affine(request):
    if request.method == 'POST':
        decrypt = False
        coefs = (int(request.POST['acoef']), int(request.POST['bcoef']))

        if request.POST['cipherEncrypt'] == 'False':
            decrypt = True
            ciphertext = request.POST['ciphertext']
            plaintext = decrypt_affine(ciphertext, coefs)
        else:
            plaintext = request.POST['plaintext']
            ciphertext = encrypt_affine(plaintext, coefs)

        return render(request, 'cypher/affine.html', {'plaintext': plaintext, 'ciphertext': ciphertext,
                                                      'decrypt': decrypt, 'acoef': coefs[0], 'bcoef': coefs[1]})

    return render(request, 'cypher/affine.html')
