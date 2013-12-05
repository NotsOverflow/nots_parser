#!/usr/bin/python
# coding=UTF-8

from core.parser import *

parser_obj = Parser("fake_sql")

char = read_single_keypress()
while True:
	parser_obj.feed(char)
	char = read_single_keypress()
