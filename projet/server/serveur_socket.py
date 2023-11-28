import socket
import threading
import os

srv_addr = os.getenv("SERVER_ADDR")
srv_port = int(os.getenv("SERVER_PORT"))


# Fonction pour gérer la communication avec chaque client
def gerer_client(client_socket, adresse_client):
    while True:
        # Recevoir des données du client
        donnees = client_socket.recv(1024)
        if not donnees:
            break

        # Afficher les données reçues
        print(f"Reçu de {adresse_client}: {donnees.decode()}")

        # Répondre au client
        reponse = "Message reçu par le serveur"
        client_socket.sendall(reponse.encode())

    # Fermer la connexion avec le client
    client_socket.close()
    print(f"Connexion avec {adresse_client} fermée")

# Créer un socket IPv4, de type SOCK_STREAM (TCP)
serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associer le socket à une adresse et un port
adresse_serveur = (srv_addr, srv_port)
serveur_socket.bind(adresse_serveur)

# Écouter jusqu'à 5 connexions simultanées
serveur_socket.listen(5)
print(f"Le serveur écoute sur {adresse_serveur}")

while True:
    # Attendre une connexion
    client_socket, adresse_client = serveur_socket.accept()
    print(f"Connexion établie avec {adresse_client}")

    # Créer un thread pour gérer la communication avec le client
    client_thread = threading.Thread(target=gerer_client, args=(client_socket, adresse_client))
    client_thread.start()