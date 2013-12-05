#!/usr/bin/env python
# -*- coding: utf-8 -*- 


class Parser:
	
	def __init__(self,name):
	
		self.rules = []
		self.buffer = ""
		self.full_sentence = ""
		self.flags = [ 0,0,0,0 ] # secces , nl , end_instrc, interupt
		self.eatch_run = ""
		self.load_functions("function_fld.%s" % name)
		self.load_rules("rules_fld/%s" % name)

	def load_functions(self,function_name):
		exec "from %s import *" % function_name
	
	def load_rules(self,file_name):
		f = open( file_name, "r" )
		for line in f:
			line = line.strip().split(":")
			self.rules.append( line )
			if line[0] == "*":
				self.eatch_run = line[1]
			
		f.close()
	
	def feed(self,char):
		self.buffer = self.buffer + char
		self.full_sentence = self.full_sentence + char
		for rule in self.rules:
			if rule[0] == ".":
				if rule[1] == char :
					exec(rule[3])
			if rule[0] == ".+":
				if (type(rule[1]) == str) and (self.buffer == rule[1]):
					exec(rule[3])
			if rule[0] == "+.":
				if (type(rule[1]) == list):
					if self.check_if_match_list(rule[1]):
						exec(rule[3])
		exec(self.eatch_run)

	def check_if_match_list(self,the_list):
		cursor = 0
		next_cursor = 0
		max_len = len(self.full_sentence)
		until = False
		for item in the_list:
			if item != "*" and until == False:
				next_cursor = cursor + len(item)
				if self.full_sentence[cursor,next_cursor] != item:
					return False
				cursor = next_cursor
			else:
				until = True 	
			if until == True:
				next_cursor = cursor + len(item)
				while self.full_sentence[cursor,next_cursor] != item :
					cursor = cursor + 1 ;
					if cursor > max_len :
						return False
					next_cursor = next_cursor + 1
				until = False
				cursor = next_cursor
		return True
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
