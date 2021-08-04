from django.shortcuts import render
from .utils.monoalphabetic.caesar import encrypt_caesar, decrypt_caesar


def caesar(request):
    if request.method == 'POST':
        caesarList = False
        decrypt = False

        if request.POST['caesarEncrypt'] == 'False':
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
