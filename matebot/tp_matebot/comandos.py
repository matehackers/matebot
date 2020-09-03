# vim:fileencoding=utf-8

import importlib,json
from matebot.plugins.log import log_str

def parse(args):
  config = args['config']
  try:
    bot_dict = {'handle': u"matebot", 'name': u"MateBot"}
    if 'bot' in args.keys():
      bot_dict = {
        'handle': args['bot'].getMe()['username'],
        'name': args['bot'].getMe()['first_name'],
      }
    args.update(
      {
        'info_dict': config['info'],
        'bot_dict': bot_dict,
        'addr_dict': config['info']['donate'],
        'plugins_list': config['plugins']['omega'],
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
      'response': u'Erro processando o comando. Os desenvolvedores foram ou \
        deveriam ter sido avisados.',
      'debug': u'Exceção %s\ncommand_list: %s' % (e, str(args['command_list'])),
      'multi': False,
      'parse_mode': None,
    }

  ## TODO acho que dá pra diminuir essas 20 linhas em uma só né?
  ## FIXME se tu acha então faz
  if args['from_id'] in config['users']['alpha']:
    args['plugins_list'].extend(config['plugins']['alpha'])
  if args['chat_id'] in config['users']['alpha']:
    args['plugins_list'].extend(config['plugins']['alpha'])
  if args['from_id'] in config['users']['beta']:
    args['plugins_list'].extend(config['plugins']['beta'])
  if args['chat_id'] in config['users']['beta']:
    args['plugins_list'].extend(config['plugins']['beta'])
  if args['from_id'] in config['users']['gamma']:
    args['plugins_list'].extend(config['plugins']['gamma'])
  if args['chat_id'] in config['users']['gamma']:
    args['plugins_list'].extend(config['plugins']['gamma'])
  if args['from_id'] in config['users']['delta']:
    args['plugins_list'].extend(config['plugins']['delta'])
  if args['chat_id'] in config['users']['delta']:
    args['plugins_list'].extend(config['plugins']['delta'])
  if args['from_id'] in config['users']['epsilon']:
    args['plugins_list'].extend(config['plugins']['epsilon'])
  if args['chat_id'] in config['users']['epsilon']:
    args['plugins_list'].extend(config['plugins']['epsilon'])
  ## Outra(o) usuária(o)
  if int(args['chat_id']) > 0:
    args['plugins_list'].extend(config['plugins']['omega'])
  ## Outro grupo
  if int(args['chat_id']) < 0:
    args['plugins_list'].extend(config['plugins']['omega'])

  ## TODO Comentando jeito antigo
  # ~ comando = str(args['command_list'].split(' ')[0].split(
    # ~ '/', 1)[1].split('@', 1)[0])
  comando = str(args['command_list'].split(' ')[0])

  ## TODO presumindo telegram
  if not args['command_type'] == "curses":
    comando = str(comando.split('/', 1)[1].split('@', 1)[0])
  args.update(command_list = args['command_list'].split(' ')[1::])

  response = u"Vossa excelência não terdes autorização para usar este comando, \
    ou o comando não existe."
  debug = u"Nada aconteceu."
  msg_type = "nada"

  for plugin in args['plugins_list']:
    try:
      return getattr(
        importlib.import_module(
          '.'.join(['matebot', 'plugins', plugin])
        ),
        '_'.join([u"cmd", comando])
      )(args)
      ## Pra que (args) aqui?
      ## Entendi! É pra enviar como argumento para o plugin/comando
    except AttributeError as e:
      if args['command_type'] == "curses":
        args['stdscr'].addstr(log_str.err(u"%s\n" % (e)))
        args['stdscr'].refresh()
      else:
        print(log_str.err(e))
      pass
    except ImportError as e:
      if args['command_type'] == "curses":
        args['stdscr'].addstr(log_str.err(u"%s\n" % (e)))
        args['stdscr'].refresh()
      else:
        print(log_str.err(e))
      pass
    except Exception as e:
      response = u"Erro processando o comando. Os desenvolvedores foram ou \
        deveriam ter sido avisados."
      debug = u"Exceção %s, command_list: %s" % (
        str(e),
        str(args['command_list']),
      )
      msg_type = "erro"
      raise
  return {
    'status': False,
    'type': msg_type,
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }
