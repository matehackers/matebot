# vim:fileencoding=utf-8

import importlib

try:
  import configparser
except ImportError:
  import ConfigParser

from plugins.log import log_str

#from plugins import *

## TODO: Reinventar este módulo pra permitir ativar e desativar plugins, atribuir permissões de uso de plugins, e o que mais eu não consigo pensar agora

def geral(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis):
  comando = str(command_list[0].split("/")[1])
  for plugin in plugins_disponiveis.split(','):
    try:
      return getattr(importlib.import_module('.'.join(['plugins', plugin])), comando)(info_dict, bot_dict, addr_dict, command_list[1:])
    except AttributeError:
      pass
    except ImportError:
      pass
  return {
    'status': False,
    'type': 'nada',
    'response': u'Esta mensagem nunca deve aparecer no telegram',
    'debug': 'Nada aconteceu. command_list: %s' % (str(command_list)),
  }

def regular_user(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis):
  return geral(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis)

def regular_group(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis):
  return geral(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis)

def admin_user(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis):
  comando = str(command_list[0].split("/")[1])
  for plugin in plugins_disponiveis.split(','):
    try:
      print(u'Testando %s em %s' % (comando, plugin))
      return getattr(importlib.import_module('.'.join(['plugins', plugin])), comando)(info_dict, bot_dict, addr_dict, command_list[1:])
    except AttributeError:
      print(u'Deu merda')
      pass
    except ImportError:
      print(u'Deu merda')
      pass
  return regular_user(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis)

def admin_group(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins):
  return regular_group(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis)

def parse(chat_id, from_id, command_list):
  config_file = str("config/.matebot.cfg")
  try:
    config = configparser.ConfigParser()
  except NameError:
    config = ConfigParser.ConfigParser()
  try:
    config.read(config_file)
    plugins_disponiveis = config.get("bot", "plugins")
    plugins_admin = config.get("bot", "plugins_admin")
  except configparser.Exception as e:
    return {
      'status': False, 
      'type': 'erro', 
      'response': u'Erro do config parser', 
      'debug': u'Erro do configparser: %s' % (e),
    }
  ## TODO: rever parâmetros dos métodos
  ## Se chat_id for negativo, estamos falando com um grupo.
  if int(chat_id) < 0:
    ## Grupo de administração
    if str(chat_id) == str(config['admin']['group']):
      return admin_group(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')), plugins_disponiveis)
    ## Grupo comum
    else:
      return regular_group(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')), plugins_disponiveis)
  ## Admnistrador
  elif str(chat_id) == str(config['admin']['id']):
    return admin_user(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')), plugins_admin)
  ## Usuário comum
  else:
    return regular_user(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')), plugins_disponiveis)

