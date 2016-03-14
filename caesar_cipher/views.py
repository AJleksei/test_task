# -*- coding:utf-8 -*-

from django.shortcuts import render

letters = [chr(x) for x in range(ord('a'), ord('z') + 1)]
encode = u'encode'
decode = u'decode'

def index(request):
    args = {}
    if request.POST:
        text = request.POST['text']
        shift = int(request.POST['shift'])
        res = ''
        if encode in request.POST:
            res = encode_caesar(text, shift)
        if decode in request.POST:
            res = decode_caesar(text, shift)
        args['res'] = res

    return render(request, 'index.html', args)


def decode_caesar(encode_text, rot):
    alphabet = len(letters)
    decode_text = ''
    # В цикле проходим по всем символам
    for encode_symbol in encode_text:
        # Если символ есть в словаре шифруемых символов
        if encode_symbol in letters:
            # Дешифруем символ
            tmp = (letters.index(encode_symbol) - rot + alphabet) % alphabet
            decode_text += letters[tmp]
        # Если сивола нет в списке шифруемых символов
        else:
            # Записываем символ без дешифрования
            decode_text += encode_symbol
    return decode_text


def encode_caesar(decode_text, rot):
    alphabet = len(letters)
    encode_text = ''
    # В цикле проходим по всем символам
    for decode_symbol in decode_text:
        # Если символ есть в словаре шифруемых символов
        if decode_symbol in letters:
            # Шифруем символ
            tmp = (letters.index(decode_symbol) + rot) % alphabet
            encode_text += letters[tmp]
        # Если сивола нет в списке шифруемых символов
        else:
            # Записываем символ без шифрования
            encode_text += decode_symbol
    return encode_text

