import enet
import pickle

class Packet:

    def __init__(self, bytes_data = b""):
        if bytes_data:
            self.data = pickle.loads(bytes_data)
        else:
            self.data = []
    
    def write(self, object):
        self.data.append(pickle.dumps(object))
    
    def read(self):
        return pickle.loads(self.data.pop(0))
    
    def to_bytes(self):
        return pickle.dumps(self.data)

###############################################################################

class Handler:

    def on_connect(self, client_id):
        pass

    def on_disconnect(self, client_id):
        pass

    def handle_packet(self, packet):
        pass

###############################################################################

class Client:

    def __init__(self, host, port):
        # Connect
        self.host = enet.Host(None, 1, 0, 0, 0)
        self.peer = self.host.connect(enet.Address(host.encode("utf-8"), port), 1)

        # Wait up to 5 seconds for connection to succeed
        event = self.host.service(5000)
        if event.type == enet.EVENT_TYPE_CONNECT:
            print("Successfully connected to server.")
        else:
            raise Exception("Failed to connect to server")

        # Receive client ID from server
        event = self.host.service(1000)
        if event.type == enet.EVENT_TYPE_RECEIVE:
            self.client_id = pickle.loads(event.packet.data)
            print("Client ID is "+str(self.client_id))
        else:
            raise Exception("Failed to receive client ID from server.")

        # Other stuff
        self.handlers = []
    
    def send(self, packet):
        self.peer.send(0, enet.Packet(packet.to_bytes()))

    def add_handler(self, handler):
        self.handlers.append(handler)
    
    def disconnect(self):
        self.peer.disconnect()
    
    def update(self):
        for i in range(100):
            event = self.host.service(0)
            if event.type == enet.EVENT_TYPE_NONE:
                break

            if event.type == enet.EVENT_TYPE_DISCONNECT:
                print("Disconnected from server.")
                break
            elif event.type == enet.EVENT_TYPE_RECEIVE:
                for handler in self.handlers:
                    packet = Packet(event.packet.data)
                    handler.handle_packet(packet, 0)


###############################################################################

class Server:
    
    def __init__(self, port):
        self.host = enet.Host(enet.Address(b"localhost", port), 10, 0, 0, 0)
        self.peers = {} # Map client IDs to peers
        self.handlers = []
        self.next_client_id = 1

    def add_handler(self, handler):
        self.handlers.append(handler)
    
    def update(self):
        for i in range(100):
            event = self.host.service(0)
            if event.type == enet.EVENT_TYPE_NONE:
               break 

            client_id = str(event.peer.address)
            if event.type == enet.EVENT_TYPE_CONNECT:
                print("Client "+str(client_id)+" connected from " + str(event.peer.address))
                # Send client ID
                event.peer.send(0, enet.Packet(pickle.dumps(client_id)))
                # Handle connection
                self.peers[client_id] = event.peer
                for handler in self.handlers:
                    handler.on_connect(client_id)
                self.next_client_id += 1
            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                print("Client "+str(client_id)+" has disconnected.")
                for handler in self.handlers:
                    handler.on_disconnect(client_id)
            elif event.type == enet.EVENT_TYPE_RECEIVE:
                for handler in self.handlers:
                    packet = Packet(event.packet.data)
                    handler.handle_packet(packet, client_id)
