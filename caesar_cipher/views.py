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
            res = automatic_encode_decode_caesar(text, shift, encode)
        if decode in request.POST:
            res = automatic_encode_decode_caesar(text, shift, decode)
        args['res'] = res

    return render(request, 'index.html', args)


def automatic_encode_decode_caesar(text, rot, action):
    def action_symbol(symbol, rot, action):
        alphabet = len(letters)
        if action == decode:
            res = ((letters.index(symbol) - rot + alphabet) % alphabet)
            return res
        if action == encode:
            res = ((letters.index(symbol) + rot) % alphabet)
            return res

    result_text = ''
    # В цикле проходим по всем символам
    for symbol in text:
        # Если символ есть в словаре шифруемых символов
        if symbol in letters:
            # Шифруем/дешифруем символ
            symbol_index = action_symbol(symbol, rot, action)
            result_text += letters[symbol_index]
        # Если сивола нет в списке шифруемых символов
        else:
            # Записываем символ без изменений
            result_text += symbol
    return result_text



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

