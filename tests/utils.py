from os.path import dirname, abspath
from socket import socket, error
from errno import EADDRINUSE

FOLDER_PATH = abspath(dirname(__file__))

def socket_status(host, port):
  try:
    socket().bind((host, port),)
    # False if the is free
    return False
  except error, (num, err):
    if num == EADDRINUSE:
      # True if the isn't free
      return True
