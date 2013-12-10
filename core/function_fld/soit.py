#!/usr/bin/python
# coding=UTF-8
from __future__ import print_function
import termios, fcntl, sys, os


def rtn(self):
	if self.run():
		reinit(self)
		self.flush()
		#put flag return line to 1
	else:
		nl(self)
		printstr(self," unknow command : %s " % self.full_sentence)
		nl(self)
		self.flush()
		reinit(self)
	self.flags[4] = 1


def errase(self,char):
	self.flags[3] = 1
	if self.selector == return_cursor_pos_relative(self) :
		mouve_selector_left(self)
		save_selector(self)
		rem_cursor_pos(self)
		printchar(self," ",False)
		restaure_selector(self)
		self.rem_char_from_sentence()
		self.buffer = get_prev_arg(self)
	else:
		if self.selector > (self.ps1_l+1):
			stemp = self.selector - (self.ps1_l+1)
			temp = "%s" % (self.full_sentence)
			self.flush()
			self.full_sentence = "%s%s" % (temp[:stemp-1], temp[stemp:])
			self.buffer = get_prev_arg(self)
			mouve_selector_left(self)
			save_selector(self)
			printstr(self, "%s " % temp[stemp:],False)
			rem_cursor_pos(self)
			restaure_selector(self)



def rem_cursor_pos(self,value=1):
	tmp = self.cursor_pos - value
	while tmp < 0 :
		tmp = tmp + self.ps1_max
		self.row = self.row - 1
		if tmp < 0 and self.row == 1:
			return False
	self.cursor_pos = tmp
	return True
	
		
def add_cursor_pos(self,value=1):
	temp = self.cursor_pos + value
	if temp > self.ps1_max :
		while temp > self.ps1_max :
			temp = temp - self.ps1_max
			self.row = self.row + 1
	self.cursor_pos = temp

def quit_interupt():
	print()
	quit()

def load_prev_to_buff(self):
	
	arg = get_prev_arg(self)
	if arg == False:
		return False
	length = len(arg)
	self.buffer = arg
	if self.rem_char_from_sentence(length):
		return True
	return False
	

def mouve_selector_right(self,n=1,opt=True):
	while n != 0:
		if self.selector < return_cursor_pos_relative(self):
			temp = self.selector
			while temp >= self.ps1_max :
				temp = temp - self.ps1_max
			if temp == 1:
				printstr(self,"\x1b[1B",False)
				printstr(self,"\x1b[%sD" % ( self.ps1_max ),False)
			else:
				printstr(self,"\x1b[1C",False)
			if opt == True:
				self.selector = self.selector + 1
		else:
			return False
		n = n - 1
	return True

def mouve_selector_left(self,n=1,opt=True):
	while n != 0:
		if self.selector > (self.ps1_l + 1):
			if self.selector <= self.ps1_max :
				printstr(self,"\x1b[1D",False)
			else:
				temp = self.selector
				while temp > self.ps1_max :
					temp = temp - self.ps1_max
				if temp == 1:
					printstr(self,"\x1b[1A",False)
					printstr(self,"\x1b[%sC" % (self.ps1_max - 1),False)
				else:
					printstr(self,"\x1b[1D",False)
			if opt == True:
				self.selector = self.selector - 1
		else:
			return False
		n = n - 1
	return True

def arrow(self,char):
	self.flags[3] = 1
	ret = sys.stdin.read(2)
	if ret == "[A":
		pass
	if ret == "[C":
		mouve_selector_right(self)
	if ret == "[B":
		pass
	#d for left
	if ret == "[D":
		mouve_selector_left(self)
	
def printstr(self,s,count=True):
    for c in s:
        printchar(self,'%c' % c,count)
        
def printchar(self,c,count=True):

	if count == False:
		print(c,end='')
		return True
		
	if self.cursor_pos == 1 or c == '\n':
		if self.row > 0:
			print('\n',end='')
		else:
			self.row = 1
		
		
	if self.selector == return_cursor_pos_relative(self) and c != '\n':
			print(c,end='')
			add_cursor_pos(self)
			self.selector = self.selector + 1
	else:
		if self.selector >= (self.ps1_l+1):
			self.buffer = ""
			self.rem_char_from_sentence()
			stemp = self.selector - ( self.ps1_l + 1 )
			self.full_sentence = "%s%s%s" % (self.full_sentence[:stemp],c, self.full_sentence[stemp:])
			cleanit(self,self.full_sentence)
			cleanit(self,self.full_sentence[:stemp+1])
			add_cursor_pos(self,len(self.full_sentence[stemp+1:]))
			
			
			printtofile("relative: %s - cursor_pos: %s - selector: %s\nrow: %s  - full: '%s' - buff: '%s'" % (return_cursor_pos_relative(self),self.cursor_pos,self.selector,self.row,self.full_sentence,self.buffer))
		#quit()

def cleanit(self,add = False):
	if self.row > 1:
		printstr(self,"\x1b[%sA" % (self.row - 1),False)
	if self.selector > 1:
		printstr(self,"\x1b[%sD" % (self.selector - 1),False)
	reinit(self)
	if add != False:
		printstr(self,"%s" % add)
			
			

def read_single_keypress(self):

    fd = sys.stdin.fileno()
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    attrs = list(attrs_save)
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK 
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR 
                  | termios.ICRNL | termios.IXON )
    attrs[1] &= ~termios.OPOST
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    try:
        ret = sys.stdin.read(1) 
    except KeyboardInterrupt: 
        ret = 0
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
	#printstr(self,ret)
	printtofile("relative: %s - cursor_pos: %s - selector: %s\nrow: %s - " % (return_cursor_pos_relative(self),self.cursor_pos,self.selector,self.row))
    return ret

def printtofile(s):
	f = open("file",'w')
	f.write(s)
	f.close()

def get_prev_arg(self):
	index = -1
	pos = index
	if len(self.full_sentence) < 1 :
		return False
	for c in self.full_sentence:
		index = index + 1
		if c == self.argsep :
			pos = index
	if pos > -1:
		return self.full_sentence[pos+1:]
	return self.full_sentence

def return_cursor_pos_relative(self):
	return ((self.row - 1) * self.ps1_max ) + self.cursor_pos 

def save_selector(self):
	printstr(self,"\x1b7" ,False)
	
def restaure_selector(self):
	printstr(self,"\x1b8" ,False)
	
def nl(self):
	printchar(self,"\n")

def reinit(self):
	self.row = 0
	self.cursor_pos = 1
	self.selector = 1
	printstr(self,"%s" % self.ps1)
	

def __init__(self):
	self.sql_items = ""
	self.sql_item_t = []
	self.sql_table = ""
	self.sql_table_t = []
	self.flags[5] = 1
	self.ps1 = "SoIt ~> "
	self.ps1_l = len(self.ps1)
	self.ps1_max = 80
	self.row = 0
	self.cursor_pos = 1
	self.selector = 1
	reinit(self)
