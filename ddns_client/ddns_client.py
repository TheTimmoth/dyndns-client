from time import strftime
import socket
import ssl

from .io_ import read_file
from .servers import Servers


class DDNSClient():
  def __init__(self, servers_path: str):
    servers = Servers(read_file(servers_path))
    for s in servers:
      for a in servers[s]["addresses"]:
        print(strftime("%Y-%m-%d %H:%M:%S ") + f"Updating {s} {a}")
        host = (a, servers[s]["port"])
        secret = servers[s]["secret"]
        self.update_dns(host, secret)

  def update_dns(self, conn, secret):
    s = socket.create_connection(conn)
    context = ssl.create_default_context()
    context.options |= ssl.OP_NO_SSLv2
    context.options |= ssl.OP_NO_SSLv3
    context.options |= ssl.OP_NO_TLSv1
    context.options |= ssl.OP_NO_TLSv1_1
    context.options |= ssl.OP_NO_TLSv1_2
    ss = context.wrap_socket(s, server_hostname="kate.2137.eu")

    ss.sendall(bytes(secret.encode("utf-8")))
    addr = ss.recv(1024).decode("utf-8")
    if addr:
      print(strftime("%Y-%m-%d %H:%M:%S ") + f"Own address is {addr}")

    if ss:
      ss.close()
    if s:
      s.close()
