# vim:fileencoding=utf-8
## Return message digest / secure hash of given string in a given algorithm
## This uses hashlib - https://docs.python.org/3/library/hashlib.html

import hashlib

def get_hashes():
  return ', '.join(sorted(hashlib.algorithms_guaranteed)).lower()

def return_hash(algo, text):
  algo = algo.lower()
  if algo in [testing.lower() for testing in hashlib.algorithms_guaranteed]:
    return u"hash %s de %s:\n\n%s" % (algo, text, getattr(hashlib, algo, None)(text.encode('utf-8')).hexdigest())
  else:
    return u'Desculpe, estou rodando em um servidor sem suporte para \'%s\', ou \'%s\' não é um algoritmo.\n\nAlgoritmos suportados: %s' % (algo, algo, get_hashes())

