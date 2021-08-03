from django.shortcuts import render
from .utils.monoalphabetic.caesar import encrypt_caesar


def caesar(request):
    if request.method == 'POST':
        plaintext = request.POST['plaintext']
        shift = int(request.POST['shift'])
        ciphertext = encrypt_caesar(plaintext, shift)

        return render(request, 'cypher/caesar.html', {'plaintext': plaintext, 'shift': shift, 'ciphertext': ciphertext})

    return render(request, 'cypher/caesar.html')
