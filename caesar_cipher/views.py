# -*- coding:utf-8 -*-
from decimal import Decimal

from django.http.response import JsonResponse, HttpResponse, \
    HttpResponseBadRequest
from django.shortcuts import render
import json


encode = u'encode'
decode = u'decode'
start_english_symbol = u'a'
end_english_symbol = u'z'


from django.views.decorators.csrf import csrf_exempt
# Словарь с символами которые разрешено шифровать/дешифровать
letters = [chr(x) for x in range(ord(start_english_symbol), ord(end_english_symbol) + 1)]


def test(request):
    data = {}
    errors = {}
    if request.is_ajax():
        data_json = json.loads(request.body)
        text = data_json.get('text', None)
        rot_str = data_json.get('rot', None)
        rot = None
        action = data_json.get('action', None)

        if not rot_str:
            errors['rot'] = u'ROT не заполнено'
        if rot_str:
            try:
                rot = int(rot_str)
            except ValueError:
                errors['rot'] = u'ROT должен быть числом'

        if not text:
            errors['text'] = u'Введите текст'

        if not action:
            errors['action'] = u'Выберите действие'

        if errors:
            payload = {'success': False, 'message': 'Error!!!!!', 'data': None }
            data_json = {'success': False, 'response': errors, 'result': 'error', 'status': '503'}
            return HttpResponseBadRequest()
            #return HttpResponse(json.dumps(data), content_type='application/json')

        if action == decode:
            data['text'], data['letters_count'] = decode_caesar(text, rot)
            data['guess_rot'] = find_cesar_key(text)
        if action == encode:
            data['text'], data['letters_count'] = encode_caesar(text, rot)
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse(status=400, content_type='application/json')


def find_cesar_key(text):
    # Длинна шифрованного текста
    text_len = len(text)
    # Относительная частота букв в тексте, в английском языке
    letters_english = {
        'a': 8.17,
        'b': 1.49,
        'c': 2.78,
        'd': 4.25,
        'e': 12.70,
        'f': 2.23,
        'g': 2.02,
        'h': 6.09,
        'i': 6.97,
        'j': 0.15,
        'k': 0.77,
        'l': 4.03,
        'm': 2.41,
        'n': 6.75,
        'o': 7.51,
        'p': 1.93,
        'q': 0.10,
        'r': 5.99,
        's': 6.33,
        't': 9.06,
        'u': 2.76,
        'v': 0.98,
        'w': 2.36,
        'x': 0.15,
        'y': 1.97,
        'z': 0.07
    }

    # Сумма абсолютных разностей частот букв в английском алфавите и в тексте
    # (различие между значениями переменных)
    min_delta = 0
    caesar_key = 0
    for i in range(0, 26):
        letter_count = frequency_letters(text, i)
        delta = 0
        # Буква, Относительная частота букв в английском языке
        for letter, quantity_english in letters_english.iteritems():
            quantity_text = float(letter_count[letter] * 100)/text_len
            # Суммируем разности частот букв
            delta += abs(quantity_text - quantity_english)
        if delta < min_delta or i == 0:
            min_delta = delta
            caesar_key = i
        # Удалить
        print '{} = {}'.format(i, delta)

    return caesar_key


def index(request):
    args = {}
    """
    if request.is_ajax():
        if request.POST:
            return test(request)

    if request.POST:
        print request.POST
        original_text = request.POST['text']
        rot = int(request.POST['rot'])
        action = request.POST['action']
        res = ''
        letters_count = {}
        if encode in request.POST:
            res, letters_count = automatic_encode_decode_caesar(original_text, rot)
        if decode in request.POST:
            res, letters_count = automatic_encode_decode_caesar(original_text, rot)
        args['res'] = res
        import json
        json_res = json.dumps({'text': res, 'letters_count': letters_count})
        args['json_res'] = json_res
    """
    return render(request, 'index.html', args)


def automatic_encode_decode_caesar(text, rot):
    letters_count = {chr(x): 0 for x in range(ord(start_english_symbol), ord(end_english_symbol) + 1)}
    len_letters = len(letters)

    result_text = ''
    # В цикле проходим по всем символам
    for symbol in text:
        is_upper = symbol.isupper()
        if is_upper:
            symbol = symbol.lower()
        # Если символ есть в словаре шифруемых символов
        if symbol in letters:
            # Шифруем/дешифруем символ
            symbol_index = ((letters.index(symbol) + rot) % len_letters)
            symbol_result = letters[symbol_index].upper() if is_upper else letters[symbol_index]
            result_text += symbol_result
            letters_count[symbol] += 1
        # Если сивола нет в списке шифруемых символов
        else:
            # Записываем символ без изменений
            result_text += symbol
    return result_text, letters_count


def frequency_letters(text, rot):
    # Количество английских букв в тексте
    letters_count = {chr(x): 0 for x in range(ord(start_english_symbol), ord(end_english_symbol) + 1)}

    len_letters = len(letters)
    # В цикле проходим по всем символам
    for symbol in text:
        symbol = symbol.lower()
        # Если символ есть в словаре шифруемых символов
        if symbol in letters:
            # Дешифруем символ
            symbol_index = ((letters.index(symbol) - rot + len_letters) % len_letters)
            decode_symbol = letters[symbol_index]
            letters_count[decode_symbol] += 1
    return letters_count


def decode_caesar(encode_text, rot):
    rot *= -1
    return automatic_encode_decode_caesar(encode_text, rot)


def encode_caesar(decode_text, rot):
    return automatic_encode_decode_caesar(decode_text, rot)



"""
def decode_caesar(encode_text, rot):
    return automatic_encode_decode_caesar(encode_text, rot, decode)

    # Количество английских букв в тексте
    letters_count = {chr(x): 0 for x in range(ord(start_english_symbol), ord(end_english_symbol) + 1)}
    len_letters = len(letters)
    decode_text = ''
    # В цикле проходим по всем символам
    for encode_symbol in encode_text:
        is_upper = encode_symbol.isupper()
        if is_upper:
            encode_symbol = encode_symbol.lower()
        # Если символ есть в словаре шифруемых символов
        if encode_symbol in letters:
            # Дешифруем символ
            symbol_index = (letters.index(encode_symbol) - rot + len_letters) % len_letters
            decode_symbol = letters[symbol_index].upper() if is_upper else letters[symbol_index]
            #decode_symbol = letters[symbol_index]
            decode_text += decode_symbol
            letters_count[encode_symbol] += 1
        # Если сивола нет в списке шифруемых символов
        else:
            # Записываем символ без дешифрования
            decode_text += encode_symbol
    return decode_text


def encode_caesar(decode_text, rot):
    return automatic_encode_decode_caesar(decode_text, rot, encode)

    # Количество английских букв в тексте
    letters_count = {chr(x): 0 for x in range(ord(start_english_symbol), ord(end_english_symbol) + 1)}
    len_letters = len(letters)
    encode_text = ''
    # В цикле проходим по всем символам
    for decode_symbol in decode_text:
        is_upper = decode_symbol.isupper()
        if is_upper:
            decode_symbol = decode_symbol.lower()
        # Если символ есть в словаре шифруемых символов
        if decode_symbol in letters:
            # Шифруем символ
            symbol_index = (letters.index(decode_symbol) + rot) % len_letters
            encode_symbol = letters[symbol_index].upper() if is_upper else letters[symbol_index]
            encode_text += encode_symbol
            letters_count[decode_symbol] += 1
        # Если сивола нет в списке шифруемых символов
        else:
            # Записываем символ без шифрования
            encode_text += decode_symbol
    return encode_text
"""