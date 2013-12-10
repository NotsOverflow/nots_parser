#! -*- coding:utf-8 -*-
 
import socket
import sys
import string
import math
 
# SETTINGS
HOST = 'irc.root-me.org'      
PORT = 6667
NICK = 'test'
IDENT = 'test2'
REALNAME = 'test212'
OWNER = 'spectre'
CHANNEL = '#Root-Me_Challenge'
BOT = 'Candy'
data = '' # sert à stocker les messages du serveur
 
 
# FONCTIONS
 
def ping(): # Répond au ping du serveur
        irc.send("PONG :Pong\n")
 
def sendmsg(msg): # fonction pour envoyer un message
        irc.send("PRIVMSG "+CHANNEL+" #"+BOT+" :"+ msg +"\n")
 
def joinchan(): # rejoindre un canal
        irc.send("JOIN "+ CHANNEL +"\n")
 
 
# CONNEXION
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket # Création du socket
print ">> connexion"
irc.connect((HOST, PORT)) # Connexion au serveur
print ">> Identification"
irc.send("USER "+IDENT+" "+HOST+"+ bla :"+REALNAME+"\n") # Identification au serveur
print ">> envoi du pseudo"
irc.send("NICK "+NICK+"\n" ) # Envoi du pseudo au serveur
print ">> connexion au channel"
joinchan() # rejoins le canal grâce à la fonction joinchan
 
 
sendmsg('!ep1')
 
 
# MAIN
while 1:
 
        ircmsg = irc.recv(2048) # récupères données du serveur
        ircmsg = ircmsg.strip('\n\r') # supprime les sauts à la ligne inutiles
 
        print(ircmsg) # affiche les messages du serveur
 
        if ircmsg.find("PING :") != -1: # si le serveur envoi un ping, on doit répondre
                ping()
 
        if ircmsg.find("PRIVSMG") != -1: # récupère message du bot
                a = ircmsg.split('/')[0] # récupères les deux nombers
                b = ircmsg.split('/')[1] # récupères les deux nombers
                r = round(math.sqrt(a) * b)
                result = "%.2f" % r
                sendmsg(result)
