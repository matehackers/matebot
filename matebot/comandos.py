# vim:fileencoding=utf-8

import importlib,json

def parse(args):
  config = args['config']
  try:
    plugins_disponiveis = config.get("bot", "plugins")
    plugins_admin = config.get("bot", "plugins_admin")
    plugins_velivery = config.get("bot", "plugins_velivery")
    plugins_velivery_admin = config.get("bot", "plugins_velivery_admin")
    velivery_pedidos_grupos = json.loads(config.get("velivery_pedidos", "grupos"))
    velivery_pedidos_usuarios = json.loads(config.get("velivery_pedidos", "usuarios"))
    velivery_admin_grupos = json.loads(config.get("velivery_admin", "grupos"))
    velivery_admin_usuarios = json.loads(config.get("velivery_admin", "usuarios"))
    cr1pt0_almoco_grupos = json.loads(config.get("cr1pt0_almoco", "grupos"))
    args.update(
      {
        'info_dict': dict(config.items('info')),
        'bot_dict': dict(config.items('bot')),
        'addr_dict': dict(config.items('crypto_addresses')),
        'plugins_list': plugins_disponiveis,
      }
    )
    args.update(command_type = 'grupo')
    if (int(args['chat_id']) > 0):
      args.update(command_type = 'mensagem')
  except Exception as e:
    raise
    return {
      'status': False,
      'type': 'erro',
      'response': u'Erro processando o comando. Os desenvolvedores foram ou deveriam ter sido avisados.',
      'debug': u'Exceção %s\ncommand_list: %s' % (e, str(args['command_list'])),
      'multi': False,
    }
  ## Administrador
  if str(args['chat_id']) == str(config['admin']['id']):
    args.update(plugins_list = plugins_disponiveis + ',' + plugins_admin)
  ## Grupo de administração
  elif str(args['chat_id']) == str(config['admin']['group']):
    args.update(plugins_list = plugins_disponiveis + ',' + plugins_admin)
  ## Grupo Velivery Admin
  elif args['chat_id'] in velivery_admin_grupos:
    args.update(plugins_list = plugins_disponiveis + ',' + plugins_velivery + ',' + plugins_velivery_admin)
  ## Usuária(o) Velivery Admin
  elif args['chat_id'] in velivery_admin_usuarios:
    args.update(plugins_list = plugins_disponiveis + ',' + plugins_velivery + ',' + plugins_velivery_admin)
  ## Grupo Velivery Pedidos
  elif args['chat_id'] in velivery_pedidos_grupos:
    args.update(plugins_list = plugins_disponiveis + ',' + plugins_velivery)
  ## Usuária(o) Velivery Pedidos
  elif args['chat_id'] in velivery_pedidos_usuarios:
    args.update(plugins_list = plugins_disponiveis + ',' + plugins_velivery)
  ## Grupo 0 (verificar descrição do grupo no arquivo de configuração)
  elif args['chat_id'] in cr1pt0_almoco_grupos:
    pass
  ## Grupo comum
  elif int(args['chat_id']) < 0:
    pass
  ## Usuário comum
  elif int(args['chat_id']) > 0:
    pass
  ## Isto nunca deveria acontecer
  else:
    pass
  
  comando = str(args['command_list'][0].split('/')[1].split('@')[0])
  args.update(command_list = args['command_list'][1:])
  for plugin in args['plugins_list'].split(','):
    print(plugin)
    try:
      return getattr(importlib.import_module('.'.join(['plugins', plugin])), comando)(args)
    except AttributeError:
      pass
    except ImportError:
      pass
    except Exception as e:
      raise
      return {
        'status': False,
        'type': 'erro',
        'response': u'Erro processando o comando. Os desenvolvedores foram ou deveriam ter sido avisados.',
        'debug': u'Exceção %s, command_list: %s' % (str(e), str(args['command_list'])),
        'multi': False,
      }
  return {
    'status': False,
    'type': 'erro',
    'response': u'Vossa excelência não terdes autorização para usar este comando, ou o comando não existe.',
    'debug': u'Nada aconteceu. command_list: %s' % (str(args['command_list'])),
    'multi': False,
  }

