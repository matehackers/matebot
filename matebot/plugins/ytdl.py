# vim:fileencoding=utf-8
#  Plugin ytdl para matebot: Devolve vídeo/áudio a partir de link.
#  Copyleft (C) 2020 Iuri Guilherme, 2020 Matehackers
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, random, validators, youtube_dl

def baixar(url):
  video_rand = '%030x' % random.randrange(16**30)
  video_file_name = '/tmp/ytdl_%s.mp4' % video_rand
  options = {
    'outtmpl' : video_file_name,
    #'format': 'worstvideo+worstaudio/worst',
    'format': 'mp4',
    #'merge_output_format': 'mp4',
    #'postprocessor_args': [
      #'-an',
      #'-c:v libx264',
      #'-crf 26',
      #'-vf scale=640:-1',
    #],
  }
  youtube_dl.YoutubeDL(options).download([url])
  return video_file_name


def cmd_y(args):
  try:
    if len(args['command_list']) > 0:
      response = u"#youtubedl"
      debug = u"[#youtubedl]: [debug] chat_id: %s, from_id: %s, message_id: %s, command_list: %s" % (
        str(args['chat_id']),
        str(args['from_id']),
        str(args['message_id']),
        str(args['command_list']),
      )
      url = ''.join(args['command_list'])
      # ~ args['bot'].sendMessage(
        # ~ args['chat_id'],
        # ~ u"Acho que encontrei o vídeo. Extraindo...",
        # ~ reply_to_message_id = args['message_id'],
      # ~ )
      # ~ args['bot'].sendMessage(
        # ~ args['chat_id'],
        # ~ u"Vídeo extraído. Enviando...",
        # ~ reply_to_message_id = args['message_id'],
      # ~ )
      video_file_name = baixar(url)
      try:
        video_file = open(video_file_name, 'rb')
        args['bot'].sendVideo(
          args['chat_id'],
          video_file,
#          duration=None,
#          width=None,
#          height=None,
#          caption=None,
#          parse_mode=None,
#          supports_streaming=None,
#          disable_notification=None,
          reply_to_message_id=args['message_id'],
#           reply_markup=None
        )
      except Exception as e:
        response = u"Não consegui enviar o vídeo por problemas técnicos. Os desenvolvedores devem ter sido avisados já, eu acho."
        debug = u"[#yotubedl]: [exception] %s" % (e)
        #raise
      finally:
        print("[#youtubedl] [debug]: closing and removing video...")
        video_file.close()
        if os.path.exists(video_file_name):
          os.remove(video_file_name)
      #video_file.close()
      #os.remove(video_file_name)
      return {
        'status': True,
        'type': 'video',
        'response': response,
        'debug': debug,
        'multi': False,
        'parse_mode': None,
        'reply_to_message_id': args['message_id'],
      }
    else:
      response = u"O comando vós já achardes. Agora me envia o comando mais um link, um URL, alguma coisa que está na world wide web e que eu possa salvar. Por exemplo:\n\n/y https://www.youtube.com/watch?v=EqSQ3mnmQ6s"
      debug = u"[#youtubedl]: [nenhum link]"
  except Exception as e:
    response = u"Não consegui extrair o vídeo por problemas técnicos. Os desenvolvedores devem ter sido avisados já, eu acho."
    debug = u"[#yotubedl]: [exception] %s" % (e)
    #raise
  return {
    'status': False,
    'type': 'erro',
    'response': response,
    'debug': debug,
    'multi': False,
    'parse_mode': None,
    'reply_to_message_id': args['message_id'],
  }

## Aliases
def cmd_youtube(args):
  return cmd_y(args)
def cmd_ytdl(args):
  return cmd_y(args)
def cmd_yt(args):
  return cmd_y(args)
def cmd_baixar(args):
  return cmd_y(args)

## Aiogram
def add_handlers(dispatcher):
  from aiogram.utils.markdown import escape_md
  from matebot.aio_matebot.controllers.callbacks import (
    command_callback,
    error_callback,
  )
  
  ## Extrai vídeo ou áudio de vários serviços
  @dispatcher.message_handler(
    commands = ['y', 'yt', 'ytdl', 'youtube', 'baixar', 'video'],
  )
  async def ytdl_callback(message):
    await message_callback(message, ['ytdl', message.chat.type])
    url = message.get_args()
    ## Será que é link?
    if url and validators.url(url):
      video_file = None
      try:
        video_file = baixar(url)
      except Exception as e:
        await error_callback(['ytdl'], e)
        command = await message.reply(
          escape_md(u"""Não consegui extrair a mídia. Olha o que o servidor me \
disse: """) + u"```{}```".format(str(e)),
          parse_mode = "Markdownv2",
          disable_notification = True,
        )
      try:
        if video_file:
          video = open(video_file, 'rb')
          await message.reply_video(
            video = video,
            caption = message.get_args(),
          )
          video.close()
          if os.path.exists(video_file):
            os.remove(video_file)
      except Exception as e:
        await error_callback(['ytdl'], e)
        command = await message.reply(u"""Não consegui enviar o arquivo. Tentei\
 avisar o pessoal do desenvolvimento...""",
          disable_notification = True,
        )
    else:
      command = await message.reply(
        u"""```\nO comando {comando} serve pra extrair um vídeo ou áudio de alg\
um site com suporte. Este comando usa o youtube-dl. Digite "{comando} url" para\
 usar (dê um espaço entre o comando e o link). Por exemplo, para baixar o vídeo\
 do rick roll:\n\n{comando} https://youtube.com/watch?v=dQw4w9WgXcQ""".format(
          message.get_command()
        ),
        parse_mode = "MarkdownV2",
      )
    await command_callback(command, ['ytdl', message.chat.type])
