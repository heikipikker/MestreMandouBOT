#!/usr/bin/env python
# coding=utf-8

import telepot, time, psutil, humanize, pprint,os, subprocess

admins = ['mthbernardes']

def get_api():
    api_key = open('api_key.txt','r').read().strip()
    return api_key

def handle_message(msg):
    user_id = msg['from']['id']
    nome = msg['from']['first_name']
    sobrenome = msg['from']['last_name']
    username = msg['from']['username']
    content_type, chat_type, chat_id = telepot.glance2(msg)
    print "ID:",user_id
    print "Nome: "+nome+' '+sobrenome
    print "Usuario: "+username
    print "Conteudo: "+content_type

    if username in admins:
        #SALVA FOTOS RECEBIDAS
        if content_type is 'photo':
            file_id = msg['photo'][len(msg['photo'])-1]['file_id']
            bot.downloadFile(file_id, 'photos/'+file_id+'.jpg')

        #SALVA VIDEOS RECEBIDOS
        elif content_type is 'voice':
            bot.downloadFile(msg['voice']['file_id'], 'voices/'+msg['voice']['file_id']+'.ogg')

        #SALVA VIDEOS RECEBIDOS
        elif content_type is 'video':
            bot.downloadFile(msg['video']['file_id'], 'videos/'+msg['video']['file_id'])

        #SALVA DOCUMENTOS RECEBIDOS
        elif content_type is 'document':
            bot.downloadFile(msg['document']['file_id'], 'documents/'+msg['document']['file_name'])

        #EXECUTA FUNCOES DE ACORDO COM O QUE FOI ENVIADO
        elif content_type is 'text':
            command = msg['text'].lower()
            print "Conteudo:"
            print command
            actions(user_id,username,nome,sobrenome,command)
    else:
        bot.sendMessage(user_id, 'Desculpe '+nome+' '+sobrenome+' nao tenho permissao para falar com voce!')
    print

def bot_help(user_id):
    bot.sendMessage(user_id,
    '''
    [+] - Comandos disponiveis - [+]

    /system reiniciar - Reinicia servidor
    /system desligar - Desliga o Servidor
    /system discos - Informacoes sobre o disco

    /services - Lista todos os serviços e o estado de cada um
    /services start nome_servico - Inicia servico
    /services stop nome_servico - Para servico
    /services restart nome_servico - Renicia servico
    /services status nome_servico - Retorna status servico'

    /apt update
    /apt upgrade
    /apt install pacote
    /apt remove pacote
    ''')


def actions(user_id,username,nome,sobrenome,command):
    command = command.split()
    if command[0] == '/system':
        if len(command) >= 2:
            if 'reiniciar' in command[1]:
                bot.sendMessage(user_id, 'Servidor sendo reiniciado!')
                os.system('shutdown -r now')

            elif 'desligar' in command[1]:
                bot.sendMessage(user_id, 'Servidor sendo desligado!')
                os.system('shutdown -h now')

            elif 'discos' in command[1]:
                for disks in psutil.disk_partitions():
                    usage = psutil.disk_usage(disks[1])
                    bot.sendMessage(user_id,
                    ('[+] - Disco - [+]'+
                    '\nDispositvo: '+disks[0]+
                    '\nMontado em: '+disks[1]+
                    '\nSistema Arquivos: '+disks[2]+
                    '\n'+
                    '\n[+] - Espaço em Disco - [+]'+
                    '\nTotal: '+str(humanize.naturalsize(usage[0]))+
                    '\nUsado: '+str(humanize.naturalsize(usage[1]))+
                    '\nlivre: '+str(humanize.naturalsize(usage[2]))+
                    '\nPercentual: '+str(usage[3])+'%\n'))
        else:
            bot_help(user_id)

    elif command[0] == '/services':
        if len(command) < 3:
            system = subprocess.check_output(['service', '--status-all'])
            bot.sendMessage(user_id, system)
        elif len(command) >= 3:
            if command[1] == 'start':
                system = subprocess.check_output(['service', command[2], command[1]])
                try:
                    bot.sendMessage(user_id, system)
                except:
                    pass
            elif command[1] == 'stop':
                system = subprocess.check_output(['service', command[2], command[1]])
                try:
                    bot.sendMessage(user_id, system)
                except:
                    pass

            elif command[1] == 'restart':
                system = subprocess.check_output(['service', command[2], command[1]])
                try:
                    bot.sendMessage(user_id, system)
                except:
                    pass

            elif command[1] == 'status':
                system = subprocess.check_output(['service', command[2], command[1]])
                try:
                    bot.sendMessage(user_id, system)
                except:
                    pass

    elif command[0] == '/apt':
        if len(command) == 2:
            if command[1] == 'update':
                system = subprocess.check_output(['apt-get', command[1]])
                try:
                    bot.sendMessage(user_id, system)
                except:
                    pass

            elif command[1] == 'upgrade':
                system = subprocess.check_output(['apt-get', command[1]])
                try:
                    bot.sendMessage(user_id, system)
                except:
                    pass

        elif len(command) == 3:
            if command[1] == 'install':
                system = subprocess.check_output(['apt-get', '-y', command[1], command[2]])
                try:
                    bot.sendMessage(user_id, system)
                except:
                    pass
            elif command[1] == 'remove':
                system = subprocess.check_output(['apt-get', '-y', command[1], command[2]])
                try:
                    bot.sendMessage(user_id, system)
                except:
                    pass
        else:
            bot_help(user_id)

    elif command[0] == '/help':
        bot_help(user_id)

    else:
        bot.sendMessage(user_id, 'Digite /help para receber uma lista dos comandos.')

api_key = get_api()
bot = telepot.Bot(api_key)
bot.notifyOnMessage(handle_message)
print 'Aguardando...'

while 1:
    time.sleep(10)
