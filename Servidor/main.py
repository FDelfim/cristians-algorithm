# Python3 program imitating a clock server
 
import socket
import datetime
   
# função para iniciar o servidor de relógio
def initiateClockServer():
 
    s = socket.socket()
    print("Socket successfully created")
       
    # Definir a porta do servidor
    port = 8000
 
    s.bind(('', port))
      
    # Definir o número máximo de conexões
    s.listen(5)     
    print("Socket is listening...")
       
    # Loop infinito para aceitar conexões
    while True:
       
       # Aceitar conexões do cliente
       connection, address = s.accept()     
       print('Server connected to', address)
       
       # Enviar a hora atual para o cliente
       connection.send(str(
                    datetime.datetime.now()).encode())
       
       # Fechar a conexão
       connection.close()
 
 
if __name__ == '__main__':
    initiateClockServer()