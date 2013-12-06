#!/usr/bin/python
# coding=UTF-8

from core.parser import *


p = Parser("fake_term")


char = p.fl.read_single_keypress()
while True:
	p.feed(char)
	char = p.fl.read_single_keypress()
