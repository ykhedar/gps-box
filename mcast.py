import socket


class MultiCastSender:
    def __init__(self, host_addr):
        self.HOST = host_addr
        self.MCAST_IP = '225.0.0.37'
        self.MCAST_PORT = 4444

        self.multicast_group = (self.MCAST_IP, self.MCAST_PORT)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        self.sock.bind(('', self.MCAST_PORT))

        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self.HOST))
        self.sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(self.MCAST_IP) + socket.inet_aton(self.HOST))

    def send_data(self, message):
        # Send data to the multicast group
        sent = self.sock.sendto(message, self.multicast_group)
        # TODO: Maybe add another condition to check if a client wants the info. When yes,
        # start sending or else don't send. This is to save network bandwidth

