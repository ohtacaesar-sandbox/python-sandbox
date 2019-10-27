import socket
from threading import Thread

PORT = 34567


def main():
  threads = [
    Thread(target=server),
    Thread(target=client),
  ]
  [t.start() for t in threads]
  [t.join() for t in threads]


def server():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
    ss.bind(("0.0.0.0", PORT))
    ss.listen(128)
    cs, (client_address, client_port) = ss.accept()
    with cs:
      print(client_address, client_port)
      while True:
        try:
          mes = cs.recv(1024)
          if len(mes) > 0:
            print(mes.decode("utf-8"))
          else:
            break
        except OSError:
          break


def client():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', PORT))
    s.sendall("あいうえお".encode("utf-8"))


if __name__ == '__main__':
  main()
