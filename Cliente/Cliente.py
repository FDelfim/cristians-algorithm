import socket
import datetime
import time
import os
from dateutil import parser
from timeit import default_timer as timer

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
        print("Synchronized process client time: " + str(client_time))
	
        # calcular o erro de sincronização
        error = actual_time - client_time
        print("Synchronization error : "+ str(error.total_seconds()) + " seconds")

        s.close()	

        # verifica o S.O do cliente
        if os.name == 'nt':
            client_time = client_time.strftime('%d/%m/%Y %H:%M:%S')
            os.system('date ' + str(client_time))
        else:
            os.system('sudo date -s "' + str(client_time) + '"')

        #faz o cliente fazer uma requisicao a cada 30 segundos
        time.sleep(30)
	



if __name__ == '__main__':
	synchronizeTime()
