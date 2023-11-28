import socket
import os

proxy_addr = os.getenv("PROXY_ADDR")
proxy_port = int(os.getenv("PROXY_PORT"))

# Créer un socket IPv4, de type SOCK_STREAM (TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Adresse du proxy auquel se connecter
adresse_proxy = (proxy_addr, proxy_port)

# Se connecter au proxy
client_socket.connect(adresse_proxy)

while True:
    # Lire l'entrée utilisateur
    message = input("Entrez un message (ou 'exit' pour quitter): ")

    # Envoyer le message au proxy
    client_socket.sendall(message.encode())

    # Quitter si l'utilisateur entre 'exit'
    if message.lower() == 'exit':
        break

    # Recevoir la réponse du proxy
    reponse = client_socket.recv(1024)
    print(f"Réponse du serveur: {reponse.decode()}")

# Fermer la connexion avec le proxy
client_socket.close()