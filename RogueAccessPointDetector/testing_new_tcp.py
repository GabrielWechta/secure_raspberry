import time
from kamene.all import send
from kamene.layers.inet import IP, TCP
from kamene.volatile import RandShort
from kamene.main import kamene_delete_temp_files


def do_3_way(destination_ip, destination_port):

    iplayer = IP(dst=destination_ip, id=1111, ttl=99)
    tcplayer = TCP(sport=RandShort(), dport=[destination_port], seq=12345, ack=1000,
                   window=1000, flags="S")
    packet = iplayer / tcplayer
    send(packet)
    time.sleep(0.1)
    kamene_delete_temp_files()
