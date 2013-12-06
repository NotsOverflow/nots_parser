#!/usr/bin/env python
# -*- coding: utf-8 -*- 


class Parser:
	
	def __init__(self,name):
	
		self.rules = []
		self.buffer = ""
		self.full_sentence = ""
		self.flags = [ 0,0,0,0,0,0 ] # secces , nl , end_instrc, interupt, no print , autoexec sentence
		self.eatch_run = ""
		self.separator = "\n"
		self.argsep = " "
		self.load_rules("core/rules_fld/%s" % name)
		self.fl = self.load_functions("function_fld.%s" % name)
		self.fl.__init__(self)

	def load_functions(self,function_name):
		return __import__(function_name, globals(), locals(), ['*'], -1)			

	
	def load_rules(self,file_name):
		f = open( file_name, "r" )
		for line in f:
			if line[0] == "#":
				continue
			line = line.strip().split(":")
			if line[1][0:3] == '"\\x' :
				line[1] = line[1][3:-1].decode('hex')
			if line[1][0:1] == '"' and line[1][-1] == '"':
				line[1] = line[1][1:-1]
			self.rules.append( line )
			if line[0] == "*":
				self.eatch_run =  "self.fl.%s" % line[1]
			if line[0] == "|":
				self.separator =  "%s" % line[1]
			
		f.close()

	def check_if_match_list(self,the_list,s=None):
		if s == None:
			s = self.full_sentence
		cursor = 0
		next_cursor = 0
		max_len = len(s)
		until = False
		for item in the_list:
			if item != "*" and until == False:
				next_cursor = cursor + len(item)
				if s[cursor,next_cursor] != item:
					return False
				cursor = next_cursor
			else:
				until = True 	
			if until == True:
				next_cursor = cursor + len(item)
				while s[cursor,next_cursor] != item :
					cursor = cursor + 1 ;
					if cursor > max_len :
						return False
					next_cursor = next_cursor + 1
				until = False
				cursor = next_cursor
		return True
		
	def exec_full_sentence_buffer(self):
		tmp = self.full_sentence.split(self.separator)
		for item in tmp:
			for rule in self.rules:
				if rule[0] == "+.":
					if (type(rule[1]) == list):
						if self.check_if_match_list(rule[1],item):
							exec("self.fl.%s" % rule[2])
							return True
					if (type(rule[1]) == str):
						if rule[1] == item.split(self.argsep)[0].lstrip(' \t\n\r').rstrip(' \t\n\r') :
							exec("self.fl.%s" % rule[2])
							return True
		return False

	def add_char_to_buffer(self,c):
		self.buffer = "%s%s" % (self.buffer,c)
		
	def rem_char_from_buffer(self,c = 1):
		if len(self.buffer) > 0:
			self.buffer = self.buffer[:-1*c]
			return True
		else:
			return False
	
	def rem_char_from_sentence(self,c = 1):
		if len(self.full_sentence) > 0:
			self.full_sentence = self.full_sentence[:-1*c]
			return True
		else:
			return False
		
	def move_to_sentence(self):
		self.full_sentence = "%s%s" % (self.full_sentence,self.buffer)
		self.buffer = ""
		return True
		
	def move_to_sentence_exec(self):
		if self.buffer != self.separator:
			self.full_sentence = "%s%s" % (self.full_sentence,self.buffer)
			self.buffer = ""
			return True
		else:
			self.flags[2] = 1
			if self.exec_full_sentence_buffer():
				self.flush()
				return True
			return False


	def flush(self):
		self.buffer = ""
		self.full_sentence = ""
		return True
		
	def feed(self,char):
		self.buffer = self.buffer + char
		for rule in self.rules:
			if rule[0] == ".":
				if rule[1] == char :
					exec("self.fl.%s" % rule[2])
			if rule[0] == ".+":
				if self.buffer == rule[1]:
					self.move_to_sentence()
					exec("self.fl.%s" % rule[2])
			if self.flags[5] == 0 and rule[0] == "+.":
				if (type(rule[1]) == list):
					if self.check_if_match_list(rule[1]):
						exec("self.fl.%s" % rule[2])
						self.flush()
		if self.flags[4] == 1:
			self.flags[4] = 0
			char = ""
			self.rem_char_from_buffer()
		else:
			code = compile(self.eatch_run,'<string>','exec')
			exec code	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
