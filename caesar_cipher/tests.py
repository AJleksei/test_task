# -*- coding:utf-8 -*-
from django.test import TestCase
from views import *


class ValidateFieldsTests(TestCase):

    def test_empty_input_parameter(self):
        data = {}
        errors = validate_fields(data)
        self.assertEqual(errors, {})

    def test_check_nonexistent_field(self):
        data = {'nonexistent_field': 22}
        errors = validate_fields(data)
        self.assertEqual(errors, {})

    def test_check_empty_rot_field(self):
        data = {'rot': ''}
        errors = validate_fields(data)
        self.assertEqual(errors, {'rot': u'ROT не заполнено'})

    def test_check_filled_rot_field(self):
        data = {'rot': 'Text example'}
        errors = validate_fields(data)
        self.assertEqual(errors, {})


class FindCesarKeyTests(TestCase):

    def test_check_filled_not_encoded_field(self):
        text = """
        In Britain today, more and more young people want to be independent
        and live apart from their parents. Some go in search of or a more
        exciting life. Others want to escape from their homes which are
        overcrowded or unhappy. Some leave home with the help of their parents,
        whilst others run away. Here is a story about one British
        young man, named Garry Davis and his way up in the life, away from home.
        """
        caesar_key = find_cesar_key(text)
        self.assertEqual(caesar_key, 0)

    def test_check_filled_encoded_field(self):
        text = """
        Pu Iypahpu avkhf, tvyl huk tvyl fvbun wlvwsl dhua av il puklwluklua
        huk spcl hwhya myvt aolpy whyluaz. Zvtl nv pu zlhyjo vm vy h tvyl
        lejpapun spml. Vaolyz dhua av lzjhwl myvt aolpy ovtlz dopjo hyl
        vclyjyvdklk vy buohwwf. Zvtl slhcl ovtl dpao aol olsw vm aolpy whyluaz,
        dopsza vaolyz ybu hdhf. Olyl pz h zavyf hivba vul Iypapzo
        fvbun thu, uhtlk Nhyyf Khcpz huk opz dhf bw pu aol spml, hdhf myvt ovtl.
        """
        caesar_key = find_cesar_key(text)
        self.assertEqual(caesar_key, 7)

    def test_empty_input_parameter(self):
        text = ''
        caesar_key = find_cesar_key(text)
        self.assertEqual(caesar_key, {})










