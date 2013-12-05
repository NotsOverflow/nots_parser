#!/usr/bin/python
# coding=UTF-8

from core.parser.py import *

parser_obj = new Parser("fake_sql")

char = read_single_keypress()
while True:
	parser_obj.feed(char)
	char = read_single_keypress()
