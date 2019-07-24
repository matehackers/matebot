# vim:fileencoding=utf-8

import importlib,json
from plugins.log import log_str

def parse(args):
  config = args['config']
  try:
    ## TODO mover tudo isto para um formato ainda mais automático que permita o 
    ## escalonamento de plugins
    ## TODO tentar entender o que eu quis dizer na frase acima
    ## TODO eu acho que eu quis dizer é que toda vez que se cria um bot novo,
    ## tem que inventar este arquivo tudo de novo. solução proposta fazer 
    ## alguma coisa que sirva para todos hipotéticos bots, e este arquivo não 
    ## precise ser editado pelo mantenedor da instância do bot.
    plugins_disponiveis = json.loads(config['plugins_listas']['geral'])
    plugins_admin = json.loads(config['plugins_listas']['admin'])
    plugins_local = json.loads(config['plugins_listas']['local'])

    bot_dict = {'handle': u"matebot", 'name': u"MateBot"}
    if 'bot' in args.keys():
      bot_dict = {
        'handle': args['bot'].getMe()['username'],
        'name': args['bot'].getMe()['first_name'],
      }
    args.update(
      {
        'info_dict': dict(config.items('info')),
        'bot_dict': bot_dict,
        'addr_dict': dict(config.items('donate')),
        'plugins_list': plugins_disponiveis,
      }
    )

    if not args['command_type'] == "curses":
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
      'parse_mode': None,
    }

  ## Administradora(e)s
  if args['chat_id'] in json.loads(config['plugins_usuarios']['admin']):
    args.update(plugins_list = args['plugins_list'] + plugins_admin)
  ## Grupo de administração
  if args['chat_id'] in json.loads(config['plugins_grupos']['admin']):
    args.update(plugins_list = args['plugins_list'] + plugins_admin)
  ## Grupos inseridos por configuração local
  if args['chat_id'] in json.loads(config['plugins_grupos']['local']):
    args.update(plugins_list = args['plugins_list'] + plugins_local)
  ## Usuária(o)s inserida(o)s por configuração local
  if args['chat_id'] in json.loads(config['plugins_usuarios']['local']):
    args.update(plugins_list = args['plugins_list'] + plugins_local)
  ## Outro grupo
  if int(args['chat_id']) < 0:
    pass
  ## Outra(o) usuária(o)
  if int(args['chat_id']) > 0:
    pass



  ## TODO Comentando jeito antigo
#  comando = str(args['command_list'].split(' ')[0].split('/', 1)[1].split('@', 1)[0])
  comando = str(args['command_list'].split(' ')[0])
  ## TODO presumindo telegram
  if not args['command_type'] == "curses":
    comando = str(comando.split('/', 1)[1].split('@', 1)[0])
  args.update(command_list = args['command_list'].split(' ')[1::])

  response = u"Vossa excelência não terdes autorização para usar este comando, ou o comando não existe."
  debug = u"Nada aconteceu. args: %s" % (str(args))

  for plugin in args['plugins_list']:
    try:
      return getattr(importlib.import_module('.'.join(['plugins', plugin])), '_'.join([u"cmd", comando]))(args)
      ## TODO Usar a linha abaixo assim que todos comandos forem atualizados
#      return getattr(importlib.import_module('.'.join(['plugins', plugin])), '_'.join([u"cmd", comando]))(args)
    except AttributeError as e:
      print(log_str.err(e))
      pass
    except ImportError as e:
      print(log_str.err(e))
      pass
    except Exception as e:
      raise
      response = u"Erro processando o comando. Os desenvolvedores foram ou deveriam ter sido avisados."
      debug = u"Exceção %s, command_list: %s" % (str(e), str(args['command_list']))
  return {
    'status': False,
    'type': "erro",
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
  }

