import socket
import ntplib
import time

# Endereço IP e porta do servidor
HOST = '192.168.0.105'
PORT = 8000

# Servidor NTP para obter a hora
ntp_server = 'pool.ntp.org'

# Cria um objeto cliente NTP
ntp_client = ntplib.NTPClient() 

# Cria um objeto socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket ao endereço IP e porta do servidor
server_socket.bind((HOST, PORT))

# Começa a escutar conexões
server_socket.listen()

print(f'Servidor de hora escutando em {HOST}:{PORT}')

while True:

    # Obtém o tempo atual a partir do servidor NTP
    response = ntp_client.request(ntp_server)

    # Obtém o timestamp da resposta e converte para a hora local
    ntp_time = time.localtime(response.tx_time)

    # Converte a hora local para uma string no formato "yyyy-mm-dd hh:mm:ss"
    time_string = time.strftime('%Y-%m-%d %H:%M:%S', ntp_time)

    # Aguarda uma conexão
    client_socket, client_address = server_socket.accept()
    print(f'Conexão recebida de {client_address}')

    # Recebe o timestamp do cliente
    client_time = float(client_socket.recv(1024).decode('ascii'))

    # Calcula o tempo de ida e volta (RTT)
    rtt = time.time() - client_time

    # Calcula a hora do servidor
    server_time = time.time() + rtt / 2.0

    # Envia a hora atual para o cliente
    client_socket.sendall(time_string.encode('ascii'))

    # Fecha a conexão com o cliente
    client_socket.close()