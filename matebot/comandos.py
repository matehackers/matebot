# vim:fileencoding=utf-8

import importlib,json

def parse(args):
  config = args['config']
  try:
    ## TODO mover tudo isto para um formato ainda mais automático que permita o escalonamento de plugins
    ## TODO tentar entender o que eu quis dizer na frase acima
    plugins_disponiveis = json.loads(config['plugins_listas']['geral'])
    plugins_admin = json.loads(config['plugins_listas']['admin'])
    plugins_velivery = json.loads(config['plugins_listas']['velivery_pedidos'])
    plugins_velivery_admin = json.loads(config['plugins_listas']['velivery_admin'])
    velivery_pedidos_grupos = json.loads(config['plugins_grupos']['velivery_pedidos'])
    velivery_pedidos_usuarios = json.loads(config['plugins_usuarios']['velivery_pedidos'])
    velivery_admin_grupos = json.loads(config['plugins_grupos']['velivery_admin'])
    velivery_admin_usuarios = json.loads(config['plugins_usuarios']['velivery_admin'])
    cr1pt0_almoco_grupos = json.loads(config['plugins_grupos']['cr1pt0_almoco'])
    args.update(
      {
        'info_dict': dict(config.items('info')),
        'bot_dict': {'handle': args['bot'].getMe()['username'], 'name': args['bot'].getMe()['first_name']},
        'addr_dict': dict(config.items('donate')),
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

  ## Administradora(e)s
  if args['chat_id'] in json.loads(config['plugins_usuarios']['admin']):
    args.update(plugins_list = plugins_disponiveis + plugins_admin)
  ## Grupo de administração
  elif args['chat_id'] in json.loads(config['plugins_grupos']['admin']):
    args.update(plugins_list = plugins_disponiveis + plugins_admin)
  ## Grupo Velivery Admin
  elif args['chat_id'] in velivery_admin_grupos:
    args.update(plugins_list = plugins_disponiveis + plugins_velivery + plugins_velivery_admin)
  ## Usuária(o) Velivery Admin
  elif args['chat_id'] in velivery_admin_usuarios:
    args.update(plugins_list = plugins_disponiveis + plugins_velivery + plugins_velivery_admin)
  ## Grupo Velivery Pedidos
  elif args['chat_id'] in velivery_pedidos_grupos:
    args.update(plugins_list = plugins_disponiveis + plugins_velivery)
  ## Usuária(o) Velivery Pedidos
  elif args['chat_id'] in velivery_pedidos_usuarios:
    args.update(plugins_list = plugins_disponiveis + plugins_velivery)
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

  comando = str(args['command_list'].split('/')[1].split('@')[0].split(' ')[0])
  comando_update = args['command_list'].split('/')
  if (len(comando_update) > 1):
    comando_grupo_update = ''.join(comando_update).split('@')
    if (len(comando_grupo_update) > 1):
      args.update(command_list = comando_grupo_update[1].split(' ')[1::])
    else:
      args.update(command_list = comando_update[1].split(' ')[1::])
  else:
    args.update(command_list = str())
  for plugin in args['plugins_list']:
    try:
      return getattr(importlib.import_module('.'.join(['plugins', plugin])), comando)(args)
    except AttributeError as e:
      pass
    except ImportError as e:
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

