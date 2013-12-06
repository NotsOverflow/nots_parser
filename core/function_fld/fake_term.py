from __future__ import print_function
#!/usr/bin/python
# coding=UTF-8

import termios, fcntl, sys, os

__all__= ["read_single_keypress","printstr","printchar","clear","rtn","quit_interupt"]

curpos = None

def read_single_keypress():

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
    return ret

def arrow(self,char):
	
	ret = sys.stdin.read(2)
	if ret == "[A":
		pass
	if ret == "[C":
		if self.cursor_pos < self.ps1_max:
			self.cursor_pos = self.cursor_pos + 1
			printstr(self,"\x1b[1C")
			self.cursor_pos = self.cursor_pos - 4
	if ret == "[B":
		pass
	if ret == "[D":
		if self.cursor_pos > self.ps1_l:
			self.cursor_pos = self.cursor_pos - 1
			printstr(self,"\x1b[1D")
			self.cursor_pos = self.cursor_pos - 4
	#printstr(self,ret)
	self.flags[4] = 1
	
def printstr(self,s):
    for c in s:
        printchar('%c' % c,self)
        
def printchar(c,self):
	if c == '\n':
		self.cursor_pos = 0;
	else:
		self.cursor_pos = self.cursor_pos + 1
	print(c,end='')
	

def clear(self):
	if (os.name == 'nt'):    
		c = os.system('cls')
	else:
		c = os.system('clear')
	del c 
	self.cursor_pos = 0;
	
def echo(self):
	printstr(self,"\n%s\n" % get_prev_arg(self))


def rtn(self):
	self.move_to_sentence()
	if self.exec_full_sentence_buffer():
		printstr(self,self.ps1)
		self.flush()
		#put flag return line to 1
	else:
		printstr(self,"\n unknow command : %s " % self.full_sentence)
		self.flush()
		printstr(self,"\n%s" % self.ps1)
	self.flags[4] = 1
	#char = read_single_keypress()
	
def quit_interupt():
	print()
	quit()

def get_next_arg(self):
	started = False
	while True:
		char = self.fl.read_single_keypress()
		printchar(char)
		if ( char == " " ) :
			if ( started == True ) :
				break
			else:
				continue
		started = True
		self.add_char_to_buffer(char)
	tmp = self.buffer
	self.add_char_to_buffer(" ")
	self.move_to_sentence()
	return tmp

def load_prev_to_buff(self):
	
	arg = get_prev_arg(self)
	if arg == False:
		return False
	length = len(arg)
	self.buffer = arg
	if self.rem_char_from_sentence(length):
		return True
	return False

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
		return self.full_sentence[pos:]
	return self.full_sentence

def errase(self,char):
	if self.rem_char_from_buffer() == False:
		if load_prev_to_buff() == False:
			return False
	#print(self.cursor_pos)
	if self.cursor_pos > self.ps1_l:
		printstr(self,"\x1b[1D \x1b[1D")
		self.cursor_pos = self.cursor_pos - 10
	self.flags[4] = 1

def fill_items_var_wn(self,char):
	printchar(char)
	self.flags[4] = 1
	self.sql_items = get_next_arg(self)
	self.sql_item_t = self.sql_items.split(',')
	
	
def fill_table_var_wn(self,char):
	printchar(char)
	self.flags[4] = 1
	self.sql_table = get_next_arg(self)
	self.sql_table_t = self.sql_items.split(',')

def get_all_info(self):
	printstr(self,"\nyou try to get %s from %s table\n" % (self.sql_items,self.sql_table))
	printstr(self,self.ps1)

def __init__(self):
	self.sql_items = ""
	self.sql_item_t = []
	self.sql_table = ""
	self.sql_table_t = []
	self.flags[5] = 1
	self.ps1 = "fake term > "
	self.ps1_l = len(self.ps1)
	self.ps1_max = 79
	self.cursor_pos = 0
	printstr(self,self.ps1)
