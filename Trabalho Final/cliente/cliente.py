import socket
import string 
import random
import pandas as pd

HOST = '192.168.100.68'
PORT = 55555

#Faz a criptografia
def encryption(data):
    coded = ''
    hash = len(data)-1
    i = hash
    while i>= 0:
        coded = coded + random.choice(string.ascii_letters)
        coded = coded + data[i]
        coded = coded + random.choice(string.ascii_letters+string.digits)    
        i -= 1
    return coded

#Faz a decriptografia
def decryption(data):
    decoded = ''
    hash = len(data)-1
    i = hash 
    i -= 1
    while i >= 0:
        decoded = decoded + data[i]
        i -= 3
    return decoded

# codifica a string criptografada de ASCII para 8B6T
def encode(data):
    encoded = ''
    table = pd.read_csv('8b6tTABLE.csv')
    table.fillna(' ', inplace = True)
    for i in range(len(data)):
        for j in range(len(table)):
            if(table['Char'].iloc[j] == data[i]):    
                encoded = encoded + flip(table['6T'].iloc[j])
    return encoded

# decodifica de 8b6T para ASCII
def decode(data):
    decoded = ''
    table = pd.read_csv('8b6tTABLE.csv')
    table.fillna(' ', inplace = True)
    i = 0
    k = 6
    while k < len(data):
        for j in range(len(table)):
            if(table['6T'].iloc[j] == flip(data[i:k])):
                decoded = decoded + table['Char'].iloc[j]
                i += 6
                k += 6
    return decoded

# muda os valores do sinal se tiver dois positivos seguidos
def flip(data):
    flipped = ''
    counter = 0
    for i in range(len(data)):
        if data[i] == '+':
            flipped = flipped + '-'
            counter += 1
        elif data[i] == '-':
            flipped = flipped + '+'
            counter -= 1
        else:
            flipped = flipped + '0'
    if counter >= 1:
        return flipped
    if counter <= -1:
        return flipped
    else: return data
    
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
s.connect((HOST, PORT))

mensagem = "Só doido nesse curso!"
mensagem = encryption(mensagem)
mensagem = encode(mensagem)

s.sendall(str.encode(mensagem))

data = s.recv(1024) 

print('Mensagem ecoada:', data.decode())