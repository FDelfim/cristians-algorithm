import socket
import datetime
import time
import os
from dateutil import parser
from timeit import default_timer as timer
import win32api

# função para sincronizar o tempo do cliente com o servidor
def synchronizeTime():

    i = 0

    while True:     
        i+=1
        print("\nRequisicao: " + str(i))
        s = socket.socket()
	
	    # porta do servidor
        port = 8000	
	
	    # conectar ao servidor
        s.connect(('192.168.0.105', port))
        request_time = timer()
	
	    # receber a hora do servidor
        server_time = parser.parse(s.recv(1024).decode())
        response_time = timer()
        actual_time = datetime.datetime.now()
        print("Hora do servidor: " + str(server_time))
        process_delay_latency = response_time - request_time
        print("Tempo de resposta: " + str(process_delay_latency) + " segundos")
        print("Hora atual do cliente: " + str(actual_time))
	
	    # sincronizar o tempo do cliente com o servidor
        client_time = server_time + datetime.timedelta(seconds = (process_delay_latency) / 2)
        print("Horário do cliente de processo sincronizado: " + str(client_time))
	
        # calcular o erro de sincronização
        error = actual_time - client_time
        print("Erro de sincronização : "+ str(error.total_seconds()) + " seconds")

        s.close()	

        # verifica o S.O do cliente
        if os.name == 'nt':
             error_seconds = error.total_seconds()
             if abs(error_seconds / 1800) < 1:
                 nova_hora = client_time.strftime("%Y,%m,%d,%w,%H,%M,%S,%j")
                 win32api.SetSystemTime(*tuple(map(int, nova_hora.split(','))))
             else:
                 while abs(error_seconds) > 1:
                     if abs(error_seconds / 1800) < 1:
                         nova_hora = client_time.strftime("%Y,%m,%d,%w,%H,%M,%S,%j")
                         win32api.SetSystemTime(*tuple(map(int, nova_hora.split(','))))
                         break
                     if error_seconds > 1:
                         nova_hora = (datetime.datetime.now() - datetime.timedelta(seconds=1800)).strftime("%Y,%m,%d,%w,%H,%M,%S,%j")
                         win32api.SetSystemTime(*tuple(map(int, nova_hora.split(','))))
                     else:
                         nova_hora = (datetime.datetime.now() + datetime.timedelta(seconds=1800)).strftime("%Y,%m,%d,%w,%H,%M,%S,%j")
                         win32api.SetSystemTime(*tuple(map(int, nova_hora.split(','))))
                     print("Atualização gradual do cliente. Erro: {} segundos".format(error_seconds))
                     time.sleep(5)
                     error_seconds = (datetime.datetime.now() - client_time).total_seconds()
        else:
            error_seconds = (datetime.datetime.now() - client_time).total_seconds()
            if abs(error_seconds/1800) < 1:
                os.system('sudo date -s "{}"'.format(client_time))
            else:
                while abs(error_seconds) > 1:
                    if abs(error_seconds/1800) < 1:
                        os.system('sudo date -s "{}"'.format(client_time))
                        break
                    if error_seconds > 1:
                        os.system('sudo date -s "{}"'.format(datetime.datetime.now() - datetime.timedelta(seconds=1800)))
                    else:
                        os.system('sudo date -s "{}"'.format(datetime.datetime.now() + datetime.timedelta(seconds=1800)))
                    print("Atualização gradual do cliente. Erro: {} segundos".format(error_seconds))
                    time.sleep(5)

                    error_seconds = (datetime.datetime.now() - client_time).total_seconds()
        time.sleep(10)
	

if __name__ == '__main__':
	synchronizeTime()
