# Thomaz Hugo Suzuki Pereira, Luan Luiz de Souza

import socket
import string 
import pandas as pd
import random
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np

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
    for k in range(len(data)):
        for j in range(len(table)):
            if(table['6T'].iloc[j] == flip(data[0:6])):
                decoded = decoded + table['Char'].iloc[j]
                data = data[6:]
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

#Constroi o grafico
#def grafico(data):
    

    #plt.figure()#figsize=(10,5))

    #r1= np.arange(len(data))

    #plt.bar(r1, data , color='#6A5ACD')#, width=barWidth)

    #plt.show()
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen()

print('Esperando conexao do client')
conn, addr = s.accept()

print('Conectado em', addr)
while True:
    data = conn.recv(1024)
    #grafico(data.decode())
    print('Mensagem 8b6t:', data.decode())
    mensagem = decode(data.decode())
    mensagem = decryption(mensagem)
    print('Mensagem traduzida: ',mensagem)
    if not data:
        print('Fechando a conexao')
        conn.close()
        break
    

    #tela
    sg.theme = 'Black'
    #layout
    layout=[
        [sg.Output(size=(60,40))]
    ]
    janela=sg.Window("Recebido",layout).Finalize()
    aux4 = encryption(mensagem)
    print(f'Mensagem 8b6t:', data.decode())
    #print(f'Mensagem criptografada: ', aux4)
    print(f'Mensagem binario:', (''.join('{:08b}'.format(ord(c)) for c in mensagem)))
    
    print(f'Mensagem traduzida: ',mensagem)

    #tela

    conn.sendall(data)
