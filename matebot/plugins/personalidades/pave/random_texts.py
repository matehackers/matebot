# vim:fileencoding=utf-8
#  Plugin personalidades para matebot: Robô também é gente?
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

### Lista de textos gerados aleatoriamente
## FIXME Sentenças adicionadas manualmente a partir das respostas de usuários.
## Nenhuma dessas frases é criação ou responsabilidade dos desenvolvedores, são
## as pessoas no Telegram ensinando a bot. Criar um sistema de filtro com banco
## de dados e machine learning vai diminuir o trabalho manual, mas também vai
## criar resultados potencialmente indesejados (por razões óbvias).

import random

from aiogram.utils.markdown import escape_md

def bebidas():
  return [
    u"bebida",
    u"bira",
    u"breja",
    u"cachaca",
    u"cachaça",
    u"cerveja",
    u"ceva",
    u"trago",
    u"vinho",
    u"uisque",
    u"uísque",
    u"whisky",
  ]

def adjetivos():
  return random.choice([
    u"gente",
  ])

def respostas_bebida():
  return random.choice([
    u"quem é que vai pagar o tragoléu de hoje?",
    u"tu que tá botando pá nois bebê?",
    u"agora sim falou o que interessa!",
    u"pudim de trago",
  ])

def respostas_ignorante(admin):
  return random.choice([
    u"???",
    u"anotei aqui",
    u"ahaha",
    u"bane aí {admin}".format(admin = admin),
    u"dane-se!",
    u"diz aí, tu {}, né?".format(random.choice([
      u"come pizza de colher",
    ])),
    u"e eu? e eu com isso!",
    u"e o kéko? o ké ko tenho a ver com isso?",
    u"eu não lembro de ter te perguntado nada",
    u"eu, hein?",
    u"fala com a mão aí \U0001f90f",
    u"fala com o batman aí \U0001f918",
    u"gurizada, me ajuda a descobrir quem é que perguntou",
    u"kkk",
    u"lista de quem te perguntou:\n[\n\n\n\n\n\n\n\n\n\n]\n.",
    u"lol",
    u"mimimi",
    u"ninguém te perguntou nada",
    u"olha ele {admin}".format(admin = admin),
    u"peraí que eu vou ver quem é que te perguntou",
    u"rsrsrs",
    u"todo mundo aqui sabe, menos tu pelo jeito, que ninguém te perguntou nada",
    u"tu respira tu e tu escreve? tu é o bichão mesmo",
  ])

def piadas():
  return respostas_ignorante('@admin')

def versiculos_md():
  return random.choice([
    u"_{verso}_\n\n*{livro}*".format(
      verso = escape_md(u"""Gazela ardorosa, corsa graciosa; que os seios da tu\
a esposa sempre te fartem de prazer, e seu amor te extasie de carinhos todos os\
 dias de tua vida."""),
      livro = escape_md(u"Provérbios 5:19"),
    ),
    u"_{verso}_\n\n*{livro}*".format(
      verso = escape_md(u"""Teus seios são como dois filhotes de cervo, como cr\
ias gêmeas de uma gazela vigorosa e que repousam entre os lírios."""),
      livro = escape_md(u"Cânticos 4:5"),
    ),
    u"_{verso}_\n\n*{livro}*".format(
      verso = escape_md(u"""Viram os filhos de Deus que as filhas dos homens er\
am formosas; e tomaram para si mulheres de todas as que escolheram."""),
      livro = escape_md(u"Gênesis 6:2"),
    ),
    u"_{verso}_\n\n*{livro}*".format(
      verso = escape_md(u"""No dia seguinte a filha mais velha disse à mais nov\
a: "Ontem à noite deitei-me com meu pai. Vamos dar-lhe vinho também esta noite,\
 e você se deitará com ele, para que preservemos a linhagem de nosso pai". Entã\
o, outra vez deram vinho ao pai naquela noite, e a mais nova foi e se deitou co\
m ele. E ele não percebeu quando ela se deitou nem quando se levantou. Assim, a\
s duas filhas de Ló engravidaram do próprio pai."""),
      livro = escape_md(u"Gênesis 19:34-36"),
    ),
    u"_{verso}_\n\n*{livro}*".format(
      verso = escape_md(u"""E vendo-a Judá, teve-a por uma prostituta, porque e\
la tinha coberto o seu rosto. E dirigiu-se a ela no caminho, e disse: Vem, peço\
-te, deixa-me possuir-te."""),
      livro = escape_md(u"Gênesis 38:15-18"),
    ),
    u"_{verso}_\n\n*{livro}*".format(
      verso = escape_md(u"""E a Palavra do SENHOR veio a mim de novo, dizendo: \
"Ó querido filho do homem; eis que havia duas mulheres, filhas da mesma mãe. E \
aconteceu que elas se prostituíram no Egito, desde muito jovens se envolveram c\
om todo tipo de perversão. Naquelas terras viram seus corpos serem tocados lasc\
ivamente; seus seios foram afagados e desvirginados."""),
      livro = escape_md(u"Ezequiel 23:1-3"),
    ),
  ])

def start(message):
  return random.choice([
    u"putz! quem é que te deu o meu contato? tô fudido",
    u"lá vem essa {adjetivo} me {interagir}".format(
      adjetivo = adjetivos(),
      interagir = random.choice([
        u"atazanar",
        u"aporrinhar",
        u"aperriar",
        u"incomodar",
        u"importunar",
        u"encher os pacová",
      ]),
    ),
    u"fala{}".format(random.choice([
      u"",
      u", bagual",
      u", chê",
      u", {adjetivo}".format(adjetivo = adjetivos()),
      u", tchê",
      u" duma vez",
    ])),
    u"tu respira tu e aperta {}? tu é o bichão mesmo".format(
      message.get_command(),
    ),
    u"""viu, todo mundo tá de prova que quem veio puxar assunto foi tu. depois \
não vem de mimimi""",
  ])

def welcome(message, bot, admin):
  return random.choice([
    u"ninguém te chamou aqui",
    u"aff, mais um pra ficar lurkando no grupo",
    u"alá {admin}, tá entrando {adjetivo} no grupo".format(
      admin = admin,
      adjetivo = adjetivos(),
    ),
    u"chegou mais um filho perdido do {admin}".format(admin = admin),
    u"é {}, pa pa pa".format(bot.get_chat_members_count(message.chat.id))
  ])
