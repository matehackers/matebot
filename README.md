MateBot
===

There is no english README. Sorry about that, I am having a mean time. Just 
learn brazilian portuguese in the meantime.  

O quê
---

Este é um [bot de Telegram](https://telegram.org/faq#bots) baseado em plugins 
escrito em [Python](https://python.org).  

[MateBot](https://github.com/matehackers/tg-matebot) foi feito para o 
hackerspace [Matehackers](https://matehackers.org).  

[Vegga](https://notabug.org/velivery/vegga) foi feita para o 
[Velivery](https://velivery.com.br).  

[Gê](https://notabug.org/greatful/great-telegram-bot) foi feita para a 
[Greatful](https://greatful.com.br).  

Matebot por sua vez é clonado de 
[CryptoForexBot](https://github.com/desci/tg-cryptoforexbot).  
Todos estes bots são inspirados na [Paloma](https://notabug.org/desci/Paloma), 
originalmente um bot de IRC inspirado na 
[lalenia](http://wiki.nosdigitais.teia.org.br/Lalenia), que é um 
[supybot](https://github.com/Supybot). Viva o software livre.  

---

Uso
---

Chame o bot em [@mate_obot](https://t.me/mate_obot) para ver a lista de 
comandos.  

Quem tiver qualquer dúvida pode entrar no 
[grupo do Matehackers no Telegram](https://t.me/matehackerspoa). Todo mundo lá 
também tem dúvidas, tu vai te sentir em casa.  

### Comandos

Atualmente o bot tem os seguintes comandos:  

#### /ajuda

Exibe os atuais comandos do bot. Atualmente quase todos exigem autenticação 
automática através do controle de acesso por id de usuário do telegram.  

**Exemplo**: `/ajuda`  

#### /doar

Exibe informações sobre como ajudar financeiramente o 
[Hackerspace Matehackers](https://matehackers.org/doar).  

#### /feedback ou /f

Envia mensagem para os desenvolvedores do bot.  

**Exemplo**: `/feedback Esse bot não funciona!`  

#### /qr

Cria uma imagem png com um QR code representando o texto que foi enviado. O 
texto pode ser qualquer coisa.  

**Exemplo**: `/qr https://matehackers.org`

#### /random ou /r

Gera um número pseudo aleatório bom para criptografia. É possível definir o 
tamanho da semente como parâmetro.  

**Exemplo**: `/random 32`

#### /pi

Gera uma boa aproximação de [pi](https://pt.wikipedia.org/wiki/Pi).  

#### /phi

Gera uma boa aproximação de [phi](https://pt.wikipedia.org/wiki/%CE%A6).  

#### /baixar ou /y

Faz download de vídeos ou áudios a partir de URLs suportadas pelo 
[youtube-dl](https://github.com/ytdl-org/youtube-dl) e envia como vídeo ou 
áudio por mensagem de telegram.  

#### /arquivo ou /a

Arquiva um site na [Wayback Machine](https://web.archive.org).  

---

Fork
---

Se vossa excelência quiserdes usar o código deste bot pra fazer o vosso 
próprio, vós deveis:  

### Entenderdes e usardes a licença GPL v3

Para mais informações, veja o arquivo [LICENSE.md](./LICENSE.md).  

### Aprenderdes a usar git

...e incidentalmente, Github ou Notabug - que são coisas completamente 
diferentes de git.  

Para mexer no código agora mesmo no Linux:  

```bash
user@home:~$ git clone -b stable https://github.com/matehackers/tg-matebot.git  
user@home:~/tg-matebot$ cd tg-matebot  
```

### Grupo de usuária(o)s e desenvolvedora(e)s

Eu criei um grupo novo para quem quiser usar, testar, desenvolver e acompanhar 
o processo de desenvolvimento, teste e uso do bot: 
<https://t.me/joinchat/CwFUFkf-dKW34FPBjEJs9Q>  

---

### Dependências

Este bot foi testado com Python 3.7; Se vós não tiverdes Python, 
[instale!](https://www.python.org/downloads/)  

Estamos usando [Flask](https://flask.palletsprojects.com/) e 
[Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot),
 então é necessário instalá-los para rodar o bot.  

Ritual de instalação:  

#### pipenv

O jeito mais fácil de todos é usar [pipenv](https://pipenv.pypa.io/), inclusive 
está incluso o Pipfile no repositório:  

```bash
user@home:~/tg-matebot$ python3 -m ensurepip  
user@home:~/tg-matebot$ python3 -m pip install --user --upgrade pip pipenv  
user@home:~/tg-matebot$ pipenv install  
```

#### Outras formas

Quem não quiser usar pipenv pode usar virtualenvwrapper, virtualenv ou outro 
método de preferência se souber o que está fazendo. Um arquivo 
`requirements.txt` é mantido atualizado no repositório.  

```bash
user@home:~/tg-matebot$ python3 -m ensurepip
user@home:~/tg-matebot$ python3 -m pip install --user --upgrade pip
user@home:~/tg-matebot$ python3 -m pip install --user -r requirements.txt
```

#### ICU

Se o bot reclamar da falta de icu:  

Debian:

```bash
user@home:~$ apt-get install libicu-dev  
```

OSX:

```bash
user@home:~$ brew install icu4c  
```

---

### Configurando

Criar o diretório *instance*:  

```bash
user@home:~/tg-matebot$ mkdir instance
```

Renomear o arquivo `doc/default_config.py` para `instance/config.py` e o 
arquivo `doc/default_env` para `.env`; sem estes arquivos, o bot não vai 
funcionar.  
Editar os arquivos, alterando o valor de `BOTFATHER_TOKEN` para o valor obtido 
através do [@BotFather](https://t.me/botfather). Alterar esta configuração no 
arquivo `.env` deve ser suficiente, mas uma configuração mais robusta é 
possível usando o arquivo `instance/config.py` pra quem conhece Flask.  
Alterar os demais campos de configuração de acordo com a necessidade, cada 
opção está comentada no arquivo de configuração de exemplo 
`doc/default_config.py`.  

```bash
user@home:~/tg-matebot$ cp doc/default_env .env
user@home:~/tg-matebot$ cp doc/default_config.py instance/config.py
```

---

### Rodando

No diretório principal do *matebot*:  

#### Desenvolvimento

Para testar o bot em um ambiente de desenvolvimento:


#### pipenv

Para rodar com pipenv, assumindo que a configuração já está correta:  

```bash
user@home:~/tg-matebot$ pipenv run flask run
```

O método antigo pra usar telepot (não recomendado, use flask e ptb):  

```bash
user@home:~/tg-matebot$ pipenv run python start.py telepot matebot
```

Este comando presume que o arquivo de configuração é 
`instance/.matebot.config.py`, renomear de acordo.  

#### Outros métodos

Quem estiver usando outra coisa que não seja pipenv, pode usar o script 
`start.py` que vai tentar encontrar os módulos e arquivos de configuração 
pertinentes. Alguns exemplos:  

```bash
user@home:~/tg-matebot$ python3 start.py flask
```

```bat
C:\Users\user\tg-matebot> Python start.py flask
```

Para parar, enviar um sinal *KeyboardInterrupt* (**CTRL+C**).  

---

### Deploy / produção

#### Systemd

Exemplo de arquivo para usar com systemd:  

```systemd
[Unit]
Description=tg-matebot daemon
After=network.target nss-lookup.target

[Service]
Type=simple
ExecStart=/home/user/.local/bin/pipenv run flask run
WorkingDirectory=/home/user/tg-matebot/
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Em um sistema Debian, este arquivo deveria estar em 
`${HOME}/.config/systemd/user/tg-matebot.service`.  

Habilitando o serviço na inicialização do sistema e iniciando agora:  

```bash
user@home:~$ systemctl --user daemon-reload  
user@home:~$ systemctl --user enable tg-matebot.service  
user@home:~$ systemctl --user -l start tg-matebot.service  
```

Para ver se está funcionando:  

```bash
user@home:~$ systemctl --user -l status tg-matebot.service  
```

Parar:  

```bash
user@home:~$ systemctl --user stop tg-matebot.service  
```

Remover da inicialização:  

```bash
user@home:~$ systemctl --user disable tg-matebot.service  
```

Reiniciar:  

```bash
user@home:~$ systemctl --user -l restart tg-matebot.service  
```

Para o caso de usar systemd como root, o arquivo de configuração deve estar em 
`/lib/systemd/system/tg-matebot.service`, e os comandos devem ser utilizados 
sem o `--user`, como por exemplo:  

```bash
root@home:/root# systemctl -l restart tg-matebot.service  
```

Mas eu não recomendo esta abordagem.  

#### Crontab

Também é possível usar cron para verificar se o bot está no ar periodicamente:  

```bash
user@home:~$ crontab -e  
```

Adicione uma linha como por exemplo esta na crontab:  

```crontab
*/10 * * * * /usr/lib/systemctl --user is-active tg-matebot.service || /usr/lib/systemctl --user restart tg-matebot.service  
```

Isto vai verificar se o bot está no ar a cada 10 minutos, e reiniciar o serviço 
caso esteja fora do ar.  

#### Docker

Eu não curto baleia azul, quem quiser fazer um dockerfile e outras atrocidades 
favor enviar pull request.  

#### Heroku / Python Anywhere

Existem usuária(o)s do bot que usam Heroku e Python Anywhere solicitando ajuda 
para configurar o robô nestes serviços. Eu nunca usei nada disto então preciso 
de ajuda para tal feito.  

---

Roadmap
---

### TODO

- [x] Traduzir este README  
  - [ ] Translate the README back to English, Pedro Bó  
- [x] Usar dicionários em todos os retornos de funções  
- [x] Melhorar o empacotamento dos plugins  
- [x] Migrar de telepot para python-telegram-bot _tag v0.1.0.0a_  
- [ ] Acrescentar também código para usar com aiogram  
- [ ] Tratar as exceções corretamente, principalmente as informativas  
  - [x] Exceções informativas para quem está tentando instalar o bot do 
    zero suficientemente tratadas e suficientemente informativas com 
    commit 367613a  
  - [ ] Usar Exception Handling do python-telegram-bot  
- [ ] Arquivos para usar com Heroku  
- [ ] Arquivos para usar com Docker  
- [ ] Documentar o roadmap com issues, milestones e projetos do github  
  - [x] Issues feitas durante uma Terça Sem Fim

---

Licença
---

Copyleft 2012-2020 Iuri Guilherme, 2017-2020 Matehackers, 2018-2019 Velivery, 
2019 Greatful, 2020 Fábrica do Futuro  

**Este programa é um software livre; você pode redistribuí-lo e/ou**  
**modificá-lo sob os termos da Licença Pública Geral GNU como publicada**  
**pela Free Software Foundation; na versão 3 da Licença, ou**  
**(a seu critério) qualquer versão posterior.**  

**Este programa é distribuído na esperança de que possa ser útil,**  
**mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO**  
**a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a**  
**Licença Pública Geral GNU para mais detalhes.**  

**Você deve ter recebido uma cópia da Licença Pública Geral GNU junto**  
**com este programa (veja o arquivo LICENSE.md).**  
**Se não, veja <http://www.gnu.org/licenses/>.**  
