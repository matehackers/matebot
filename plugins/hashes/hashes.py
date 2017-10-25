# vim:fileencoding=utf-8
## Return message digest / secure hash of given string in a given algorithm
## This uses hashlib - https://docs.python.org/3/library/hashlib.html

import hashlib

class hashes():
  def __init__(self):
    pass
  def get_hashes(self):
    return ', '.join(sorted(hashlib.algorithms_available)).lower()
  def return_hash(self, algo, text):
    if algo in hashlib.algorithms_available:
      return 'hash %s de \'%s\':\n\n%s' % (algo, text, getattr(hashlib, algo, None)(text).hexdigest())
    else:
      return u'Desculpe, estou rodando em um servidor sem suporte para \'%s\', ou \'%s\' não é um algoritmo.\n\nAlgoritmos suportados: %s' % (algo, algo, self.get_hashes())

