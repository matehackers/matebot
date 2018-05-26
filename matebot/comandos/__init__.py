# vim:fileencoding=utf-8

try:
  import configparser
except ImportError:
  import ConfigParser

from plugins.log import log_str
from matebot.comandos import anyone, admin, user

def geral(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict):
  try:
    return getattr(anyone, str(command_list[0].split("/")[1]))(info_dict, bot_dict, addr_dict, command_list[1:])
  except AttributeError:
    return {
      'status': False,
      'type': 'nada',
      'response': u'Esta mensagem nunca deve aparecer no telegram',
      'debug': 'Nada aconteceu. command_list: %s' % (str(command_list)),
    }

def regular_user(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict):
  try:
    return getattr(user, str(command_list[0].split("/")[1]))(info_dict, bot_dict, addr_dict, command_list[1::1])
  except AttributeError:
    return geral(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict)

def regular_group(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict):
  return geral(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict)

def admin_user(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict):
  try:
    return getattr(admin, str(command_list[0].split("/")[1]))(info_dict, bot_dict, addr_dict, command_list[1::1])
  except AttributeError:
    return regular_user(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict)

def admin_group(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict):
  return regular_group(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict)

def parse(chat_id, from_id, command_list):
  config_file = str("config/.matebot.cfg")
  try:
    config = configparser.ConfigParser()
  except NameError:
    config = ConfigParser.ConfigParser()
  try:
    config.read(config_file)
    ## TODO: Esta exceção deveria ser tratada na primeira vez que a gente
    ## tentar acessar uma seção do arquivo
  except configparser.NoSectionError as e:
    return {
      'status': False, 
      'type': 'erro', 
      'response': u'Erro do config parser', 
      'debug': u'Erro do configparser: %s' % (e),
    }
  ## If chat_id is negative, then we're talking with a group.
  if chat_id < 0:
    ## Admin group
    if chat_id == config['admin']['group']:
      return admin_group(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')))
    ## Regular group
    else:
      return regular_group(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')))
  ## Admin user
  elif chat_id == config['admin']['id']:
    return admin_user(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')))
  ## Regular user
  else:
    return regular_user(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')))

