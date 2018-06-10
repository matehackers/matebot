# vim:fileencoding=utf-8

import importlib,json

try:
  import configparser
except ImportError:
  import ConfigParser

from plugins.log import log_str

## TODO: Reinventar este módulo pra permitir ativar e desativar plugins, atribuir permissões de uso de plugins, e o que mais eu não consigo pensar agora

def geral(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis):
  comando = str(command_list[0].split('/')[1].split('@')[0])
  for plugin in plugins_disponiveis.split(','):
    try:
      return getattr(importlib.import_module('.'.join(['plugins', plugin])), comando)(info_dict, bot_dict, addr_dict, command_list[1:])
    except AttributeError:
      pass
    except ImportError:
      pass
    except Exception as e:
      return {
        'status': False,
        'type': 'erro',
        'response': u'Erro processando o comando. Os desenvolvedores foram ou deveriam ter sido avisados.',
        'debug': u'Exceção %s\ncommand_list: %s' % (e, str(command_list)),
        'multi': False,
      }
  return {
    'status': False,
    'type': 'erro',
    'response': u'Vossa excelência não terdes autorização para usar este comando, ou o comando não existe.',
    'debug': u'Nada aconteceu. command_list: %s' % (str(command_list)),
    'multi': False,
  }

def regular_user(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis):
  return geral(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis)

def regular_group(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis):
  return geral(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis)

def admin_user(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis, plugins_admin):
  comando = str(command_list[0].split('/')[1].split('@')[0])
  for plugin in plugins_admin.split(','):
    try:
      return getattr(importlib.import_module('.'.join(['plugins', plugin])), comando)(info_dict, bot_dict, addr_dict, command_list[1:])
    except AttributeError:
      pass
    except ImportError:
      pass
    except Exception as e:
      return {
        'status': False,
        'type': 'erro',
        'response': u'Erro processando o comando. Os desenvolvedores foram ou deveriam ter sido avisados.',
        'debug': u'Exceção %s\ncommand_list: %s' % (e, str(command_list)),
        'multi': False,
      }
  return regular_user(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis)

def admin_group(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis, plugins_admin):
  return regular_group(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis)

def velivery_user(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis, plugins_velivery):
  comando = str(command_list[0].split('/')[1].split('@')[0])
  for plugin in plugins_velivery.split(','):
    try:
      return getattr(importlib.import_module('.'.join(['plugins', plugin])), comando)(info_dict, bot_dict, addr_dict, command_list[1:])
    except AttributeError:
      pass
    except ImportError:
      pass
    except Exception as e:
      return {
        'status': False,
        'type': 'erro',
        'response': u'Erro processando o comando. Os desenvolvedores foram ou deveriam ter sido avisados.',
        'debug': u'Exceção %s\ncommand_list: %s' % (e, str(command_list)),
        'multi': False,
      }
  return regular_user(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis)

def velivery_group(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis, plugins_velivery):
  comando = str(command_list[0].split('/')[1].split('@')[0])
  for plugin in plugins_velivery.split(','):
    try:
      return getattr(importlib.import_module('.'.join(['plugins', plugin])), comando)(info_dict, bot_dict, addr_dict, command_list[1:])
    except AttributeError:
      pass
    except ImportError:
      pass
    except Exception as e:
      return {
        'status': False,
        'type': 'erro',
        'response': u'Erro processando o comando. Os desenvolvedores foram ou deveriam ter sido avisados.',
        'debug': u'Exceção %s\ncommand_list: %s' % (e, str(command_list)),
        'multi': False,
      }
  return regular_user(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis)

def group_0(chat_id, from_id, command_list, info_dict, bot_dict, addr_dict, plugins_disponiveis):
  ## TODO só pra lembrar que isto aqui não faz nada enquanto não tiver alguma coisa neste método
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
    plugins_velivery = config.get("bot", "plugins_velivery")
    grupo_velivery_pedidos = int(config.get("velivery", "grupo_pedidos"))
    ids_velivery_pedidos = json.loads(config.get("velivery", "ids_pedidos"))
    grupos = json.loads(config.get("velivery", "grupos"))
  except Exception as e:
    return {
      'status': False, 
      'type': 'erro', 
      'response': u'Erro do config parser', 
      'debug': u'Erro do configparser: %s' % (e),
      'multi': False,
    }
  ## TODO: rever parâmetros dos métodos
  print('chat_id = %s, grupo_velivery_pedidos = %s, ids_velivery_pedidos = %s, chat_id é o grupo do velivery = %s %s' % (chat_id, grupo_velivery_pedidos, ids_velivery_pedidos, (str(chat_id) == str(grupo_velivery_pedidos)), (int(chat_id) == int(grupo_velivery_pedidos))))
  ## Administrador
  if str(chat_id) == str(config['admin']['id']):
    return admin_user(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')), plugins_disponiveis, plugins_admin)
  ## Grupo de administração
  elif str(chat_id) == str(config['admin']['group']):
    return admin_group(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')), plugins_disponiveis, plugins_admin)
  ## Grupo Velivery Pedidos
  elif str(chat_id) == str(grupo_velivery_pedidos):
    return velivery_group(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')), plugins_disponiveis, plugins_velivery)
  ## Usuária(o) Velivery Pedidos
  elif chat_id in self.ids_velivery_pedidos:
    return velivery_user(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')), plugins_disponiveis, plugins_velivery)
  ## Grupo 0 (verificar descrição do grupo no arquivo de configuração)
  elif str(chat_id) == str(grupos['0']):
    return group_0(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')), plugins_disponiveis)
  ## Grupo comum
  elif int(chat_id) < 0:
    return regular_group(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')), plugins_disponiveis)
  ## Usuário comum
  elif int(chat_id) > 0:
    return regular_user(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')), plugins_disponiveis)
  ## Isto nunca deveria acontecer
  else:
    return geral(chat_id, from_id, command_list, dict(config.items('info')), dict(config.items('bot')), dict(config.items('crypto_addresses')), plugins_disponiveis)

