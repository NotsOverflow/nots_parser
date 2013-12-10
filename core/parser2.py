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
		
	def store_buffer_arg(self):
		tmp = self.buffer
		if tmp != "":
			self.full_sentence = "%s %s" % (self.full_sentence,self.buffer)
			self.buffer = ""
		return tmp
	
	def flush(self):
		self.buffer = ""
		self.full_sentence = ""
		return True
		
	def load_first_arg(self):
		index = 0
		self.store_buffer_arg()
		while self.sentence_full[index] != " ":
			 self.buffer = "%s%s" % (self.buffer, self.sentence_full[index] )
			 index = index + 1
		self.sentece_full = self.sentence_full[index:]
		
	def run(self):
		self.load_first_arg()
		for rule in self.rules:
			if rule[0] == "+.":
				if self.buffer == rule[1]:
					exec("self.fl.%s" % rule[2])
	
	def feed(self,char):
		if char == self.argsep and self.buff != "":
			for rule in self.rules:	
			self.store_buffer_arg()
			if rule[0] == ".+":
				if self.buffer == rule[1]:
					self.store_buffer_arg()
					exec("self.fl.%s" % rule[2])
		else:
			if char != self.argsep:
				self.buffer = self.buffer + char
			for rule in self.rules:
				if rule[0] == ".":
					if rule[1] == char :
						exec("self.fl.%s" % rule[2])
		if self.flags[4] == 1:
			self.flags[4] = 0
			char = ""
		else:
			code = compile(self.eatch_run,'<string>','exec')
			exec code	
		#self.fl.printtofile("%s\n" % (self.buffer))
		
		
		
		
		
		
		
		
		
		
		
		
		
		
