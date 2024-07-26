#!/usr/bin/python3
'''Test suite for AirBnB console'''
import unittest
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from io import StringIO
import os


class test_Console(unittest.TestCase):
    '''Class for testing the console'''
    def setUp(self) -> None:
        ''' '''
        pass

    def tearDown(self):
        '''tear down'''
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_create_no_args(self):
        '''test for create without args'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual(f.getvalue(), '** class name missing **\n')

    def test_creat_cls(self):
        '''test create with a class'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User')
            self.assertTrue(os.access('file.json', os.R_OK))

    def test_create_param(self):
        '''test with param'''
        val = 'koko'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User name="koko"')
        storage.reload()
        user_key = storage.all()['User.' + f.getvalue().strip()]
        self.assertEqual(user_key.__dict__['name'], val)

    def test_create_string_space(self):
        '''string with underscore'''
        val = 'koko basta'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User name="koko_basta"')
        storage.reload()
        user_key = storage.all()['User.' + f.getvalue().strip()]
        self.assertEqual(user_key.__dict__['name'], val)

    def test_create_integer(self):
        '''create integer'''
        val = 23
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User name=23')
        storage.reload()
        user_key = storage.all()['User.' + f.getvalue().strip()]
        self.assertEqual(user_key.__dict__['name'], val)

    def test_create_float(self):
        '''create float'''
        val = 23.8
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User name=23.8')
        storage.reload()
        user_key = storage.all()['User.' + f.getvalue().strip()]
        self.assertEqual(user_key.__dict__['name'], val)
