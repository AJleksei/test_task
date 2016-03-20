# -*- coding:utf-8 -*-
from decimal import Decimal

from django.http.response import JsonResponse, HttpResponse, \
    HttpResponseBadRequest
from django.shortcuts import render
import json


ENCODE = u'encode'
DECODE = u'decode'
START_ENGLISH_SYMBOL = u'a'
END_ENGLISH_SYMBOL = u'z'


# Словарь с символами которые разрешено шифровать/дешифровать
letters = [chr(x) for x in range(ord(START_ENGLISH_SYMBOL),
                                 ord(END_ENGLISH_SYMBOL) + 1)]


def coding_view(request):
    data = {}
    data_response = {}
    data_json = json.loads(request.body)
    data['text'] = data_json.get('text', None)
    data['rot'] = data_json.get('rot', None)
    data['action'] = data_json.get('action', None)

    errors = validate_fields(data)

    if not errors:
        try:
            data['rot'] = int(data['rot'])
        except ValueError:
            errors['rot'] = u'ROT должен быть числом'

    if errors:
        return HttpResponse(json.dumps(errors), status=400,
                            content_type='application/json')

    if data['action'] == DECODE:
        data_response['text'] = decode_caesar(data['text'], data['rot'])
    if data['action'] == ENCODE:
        data_response['text'] = encode_caesar(data['text'], data['rot'])
    return HttpResponse(json.dumps(data_response),
                        content_type='application/json')


def validate_fields(data):
    errors = {}
    fields = {
        'text': u'Введите текст',
        'rot': u'ROT не заполнено',
        'action': u'Выберите действие',
    }

    for field, error in fields.iteritems():
        if data.__contains__(field):
            if not data[field]:
                errors[field] = error
    return errors


def find_key_view(request):
    data = {}
    data_response = {}
    data_json = json.loads(request.body)
    data['text'] = data_json.get('text', None)

    errors = validate_fields(data)

    if errors:
        return HttpResponse(json.dumps(errors), status=400,
                            content_type='application/json')

    data_response['guess_rot'] = find_cesar_key(data['text'])
    return HttpResponse(json.dumps(data_response),
                        content_type='application/json')


def find_cesar_key(text):
    if not text:
        return {}
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

    text_len = len(text)
    # Сумма разностей частот букв в английском алфавите и в заданном тектсе
    min_delta = 0
    caesar_key = 0
    for i in range(0, len(letters)):
        # Считаем количество английских букв в тексте со смещением = i
        letters_count = frequency_letters(text, i)
        delta = 0
        for letter, quantity in letters_count.iteritems():
            # Относительная частота английских букв в заданном тексте
            quantity_text = float(quantity * 100) / text_len
            # Суммируем разности частот букв
            delta += abs(letters_english[letter] - quantity_text)
        if delta < min_delta or i == 0:
            min_delta = delta
            caesar_key = i
    return caesar_key


def index(request):
    args = {}
    return render(request, 'index.html', args)


def automatic_encode_decode_caesar(text, rot):
    len_letters = len(letters)

    result_text = ''
    for symbol in text:
        is_upper = symbol.isupper()
        if is_upper:
            symbol = symbol.lower()
        if symbol in letters:
            # Шифруем/дешифруем символ
            symbol_index = ((letters.index(symbol) + rot) % len_letters)
            symbol_result = letters[symbol_index].upper() if is_upper else letters[symbol_index]
            result_text += symbol_result
        else:
            # Записываем символ без изменений
            result_text += symbol.upper() if is_upper else symbol
    return result_text


def frequency_letters(text, rot):
    # Количество английских букв в заданном тексте
    letters_count = {chr(x): 0 for x in range(ord(START_ENGLISH_SYMBOL),
                                              ord(END_ENGLISH_SYMBOL) + 1)}

    len_letters = len(letters)
    for symbol in text:
        symbol = symbol.lower()
        if symbol in letters:
            # Дешифруем символ
            symbol_index = ((letters.index(symbol) - rot + len_letters) %
                            len_letters)
            decode_symbol = letters[symbol_index]
            letters_count[decode_symbol] += 1
    return letters_count


def decode_caesar(encode_text, rot):
    return automatic_encode_decode_caesar(encode_text, rot*-1)


def encode_caesar(decode_text, rot):
    return automatic_encode_decode_caesar(decode_text, rot)
