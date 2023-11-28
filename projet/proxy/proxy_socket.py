import socket
import threading

import os

proxy_addr = os.getenv("PROXY_ADDR")
proxy_port = int(os.getenv("PROXY_PORT"))
srv_addr = os.getenv("SERVER_ADDR")
srv_port = int(os.getenv("SERVER_PORT"))


# Fonction pour gérer la communication avec chaque client
def gerer_client(client_socket, adresse_client, serveur_socket):
    while True:
        # Recevoir des données du client
        donnees = client_socket.recv(1024)
        if not donnees:
            break

        # Afficher les données reçues
        print(f"Reçu de {adresse_client}: {donnees.decode()}")

        # Envoyer les données au serveur
        serveur_socket.sendall(donnees)

        # Recevoir la réponse du serveur
        reponse = serveur_socket.recv(1024)

        # Envoyer la réponse au client
        client_socket.sendall(reponse)

    # Fermer la connexion avec le client et le serveur
    client_socket.close()
    print(f"Connexion avec {adresse_client} fermée")

# Créer un socket IPv4, de type SOCK_STREAM (TCP)
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associer le socket à une adresse et un port
adresse_proxy = (proxy_addr, proxy_port)
proxy_socket.bind(adresse_proxy)

# Écouter jusqu'à 5 connexions simultanées
proxy_socket.listen(5)
print(f"Le proxy écoute sur {adresse_proxy}")

# Adresse et port du serveur
adresse_serveur = (srv_addr, srv_port)

while True:
    # Attendre une connexion du client
    client_socket, adresse_client = proxy_socket.accept()
    print(f"Connexion établie avec {adresse_client}")

    # Connexion au serveur
    serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur_socket.connect(adresse_serveur)

    # Créer un thread pour gérer la communication avec le client
    client_thread = threading.Thread(target=gerer_client, args=(client_socket, adresse_client, serveur_socket))
    client_thread.start()