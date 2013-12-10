#!/usr/bin/python
# coding=UTF-8

from core.parser import *


p = Parser("soit")


char = p.fl.read_single_keypress(p)
while True:
	p.feed(char)
	char = p.fl.read_single_keypress(p)
