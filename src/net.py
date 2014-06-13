import enet
import pickle

class Packet:

    def __init__(self):
        self.data = []
    
    def write(self, object):
        self.data.append(pickle.dumps(object))
    
    def read(self):
        return pickle.loads(self.data.pop(0))

###############################################################################

class NetClient:

    def __init__(self, host, port):
        self.host = enet.Host(None, 1, 0, 0, 0)
        self.peer = host.connect(enet.Address(host.encode("utf-8"), port), 1)
    
    def send(self, message):
        self.peer.send(0, enet.Packet(message))
    
    def disconnect(self):
        self.peer.disconnect()
    
    def update(self):
        for i in range(100):
            event = self.host.service(1)
            if not event:
                break

            if event.type == enet.EVENT_TYPE_CONNECT:
                print("%s: CONNECT" % event.peer.address)
            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                print("%s: DISCONNECT" % event.peer.address)
                run = False
                break
            elif event.type == enet.EVENT_TYPE_RECEIVE:
                print("%s: IN:  %r" % (event.peer.address, event.packet.data))


###############################################################################

class NetServer:
    
    def __init__(self, port):
        self.host = enet.Host(enet.Address(b"localhost", port), 10, 0, 0, 0)
    
    def update(self):
        event = self.host.service(1)
        if event.type == enet.EVENT_TYPE_CONNECT:
            print("%s: CONNECT" % event.peer.address)
            connect_count += 1
        elif event.type == enet.EVENT_TYPE_DISCONNECT:
            print("%s: DISCONNECT" % event.peer.address)
            connect_count -= 1
            if connect_count <= 0 and shutdown_recv:
                run = False
        elif event.type == enet.EVENT_TYPE_RECEIVE:
            print("%s: IN:  %r" % (event.peer.address, event.packet.data))
            msg = event.packet.data
            if event.peer.send(0, enet.Packet(msg)) < 0:
                print("%s: Error sending echo packet!" % event.peer.address)
            else:
                print("%s: OUT: %r" % (event.peer.address, msg))
            if event.packet.data == "SHUTDOWN":
                shutdown_recv = True