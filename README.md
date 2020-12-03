MateBot
===

There is no english README. Sorry about that, I am having a mean time. Just 
learn brazilian portuguese in the meantime.  

O quê
---

Este é um [bot de Telegram](https://telegram.org/faq#bots) baseado em plugins 
escrito em [Python](https://python.org).  

### Uso

Chame o bot em [@mate_obot](https://t.me/mate_obot) para ver a lista de 
comandos.  

Quem tiver qualquer dúvida pode entrar no 
[grupo do MateBot no Telegram](https://t.me/joinchat/CwFUFkf-dKW34FPBjEJs9Q). 
Todo mundo lá também tem dúvidas, tu vai te sentir em casa.  

#### Comandos

Atualmente o bot tem os seguintes comandos:  

##### /lista

Exibe os atuais comandos do bot.  

**Aliases**: `/help` `/ajuda`  

##### /doar

Exibe informações sobre como ajudar financeiramente o 
[Hackerspace Matehackers](https://matehackers.org/doar).  

**Alias**: `/donate`  

##### /feedback

Envia mensagem para os desenvolvedores do bot. É necessário enviar um texto.    

**Exemplo**: `/feedback Esse bot não funciona!`  

**Alias**: `/f`  

##### /qr

Cria uma imagem png com um QR code representando o texto que foi enviado. O 
texto pode ser qualquer coisa.  

**Exemplo**: `/qr https://matehackers.org`  

**Alias**: `/qrcode`

##### /random

Gera um número pseudo aleatório bom para criptografia. É possível definir o 
tamanho da semente como parâmetro.  

**Exemplos**: `/random` ou `/random 32`  

**Alias**: `/r`  

##### /pi

Gera uma boa aproximação de [pi](https://pt.wikipedia.org/wiki/Pi).  

##### /phi

Gera uma boa aproximação de [phi](https://pt.wikipedia.org/wiki/%CE%A6).  

##### /baixar

Faz download de vídeos ou áudios a partir de URLs suportadas pelo 
[youtube-dl](https://github.com/ytdl-org/youtube-dl) e envia como vídeo ou 
áudio por mensagem de telegram.  

**Aliases**: `/y` `/ytdl`  

##### /arquivar

Arquiva um site na [Wayback Machine](https://web.archive.org).  

**Exemplo**: `/arquivar https://matehackers.org`  

**Aliases**: `/a` `/wm` `/archive`  

Por que
---

### História

[MateBot](https://github.com/matehackers/matebot) foi feito para o hackerspace 
[Matehackers](https://matehackers.org).  

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

Como
---

### Roadmap

Ver também o arquivo [CHANGES.TXT](./CHANGES.TXT)  

#### [Versão 0.1](https://github.com/matehackers/matebot/milestones/1)

Nível de automata: 
[combinational logic](https://en.wikipedia.org/wiki/Combinational_logic)  

##### Requisitos e escopo

- [ ] Bot deve responder comandos com valores pré definidos  
- [ ] Bot pode ter personalidade fixa configurada previamente e que vai 
perdurar durante todo o seu funcionamento  
- [ ] Novas funcionalidades podem ser acrescentadas através de plugins  
- [ ] Funcionalidades podem ser ativadas ou desativadas de acordo com 
personalidade ou finalidade do bot  
- [ ] Sistema de log para depuração  

##### Funcionalidades

- [x] Geração de QR Code  
- [x] Download de vídeos do Youtube  
- [x] Geração de números aleatórios  
- [x] Cálculo de hash de textos  
- [x] Recepção de novos usuários em grupos no Telegram  
- [x] Salvar URLs na Wayback Machine  

###### Funcionalidades abandonadas

Funcionalidades presentes em forks ou versão **v0.0.14**  

- [x] Conversão de valores [**coinmarketcap**] (**cryptoforex**)  
- [x] Integração com bancos de dados externos [**velivery**] (**vegga**)  
- [x] Envio de SMS e realização de ligações telefônicas [**totalvoice**] 
(**vegga**)  
- [ ] Sistema auxiliar para produção de alimentos [**cr1pt0_almoco**]  
- [x] Integração com ESP32 e monitoramento climático (**climobike**)  
- [x] Controle de atividades de trabalho [**workrave**] (**gê**)  

#### [Versão 0.2](https://github.com/matehackers/matebot/milestone/2)

Nível de automata: 
[finite-state machine](https://en.wikipedia.org/wiki/Finite-state_machine)  

##### Requisitos e escopo

- [ ] Bot deve responder comandos de acordo com regras fixas e variáveis 
conforme aprendizado prévio  
- [ ] Bot deve ter personalidade configurada no estado inicial que pode variar 
e humor que deve variar  
- [ ] Funcionalidades podem ser ativadas ou desativadas de acordo com mudança 
de personalidade, humor ou evento de aprendizado  
- [ ] Sistema de coleta de dados para machine learning  
- [ ] Bot deve funcionar no Telegram e no Discord  

##### Funcionalidades

- [ ] Faz questionários para usuários e armazena as informações em banco de 
dados  
- [ ] Usa dados obtidos para tomar decisões e adicionar pessoas em grupos de 
acordo com critérios estabelecidos  
- [ ] Cria perfil de pessoas através de análise de respostas  
- [ ] Otimiza perfil de pessoas através de análise de comportamento  

### TODO

- [x] Traduzir este README  
  - [ ] Translate the README back to English, Pedro Bó  
- [x] Usar dicionários em todos os retornos de funções  
- [x] Melhorar o empacotamento dos plugins  
- [x] Migrar de telepot para python-telegram-bot _tag v0.1.0.0a_  
- [x] Acrescentar também código para usar com aiogram  _tag v0.1.3.0_
- [ ] Tratar as exceções corretamente, principalmente as informativas  
  - [x] Exceções informativas para quem está tentando instalar o bot do 
    zero suficientemente tratadas e suficientemente informativas com 
    commit 367613a  
  - [ ] Usar Exception Handling do python-telegram-bot  
- [ ] Arquivos para usar com Heroku  
- [x] Arquivos para usar com Docker  
- [ ] Documentar o roadmap com issues, milestones e projetos do github  
  - [x] Issues feitas durante uma Terça Sem Fim

---

Onde
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
user@home:~$ git clone https://github.com/matehackers/matebot.git  
user@home:~$ cd matebot  
user@home:~/matebot$ python3 -m pip install --user --upgrade pip pipenv
user@home:~/matebot$ pipenv install
user@home:~/matebot$ pipenv run matebot
```

### Grupo de usuária(o)s e desenvolvedora(e)s

Eu criei um grupo novo para quem quiser conversar sobre, usar, testar, 
desenvolver e acompanhar o processo de desenvolvimento, teste e uso do bot: 
<https://t.me/joinchat/CwFUFkf-dKW34FPBjEJs9Q>  

Grupo só para testar bots (pode gerar o caos): 
<https://t.me/joinchat/CwFUFhbgApLHBMLoNnkiRg>  

Grupo para testar o plugin de logs: 
<https://t.me/joinchat/CwFUFhy2NQRi_9Cc60v_aA>  

Pra testar o plugin de logs, coloque o bot neste grupo e use o chat_id 
`-481703172` no arquivo de configuração (_bot.users['special']['log']_)  

---

### Dependências

Este bot foi testado com Python 3.7 e 3.8; Se vós não tiverdes Python, 
[instale!](https://www.python.org/downloads/)  

Estamos usando [Aiogram](https://docs.aiogram.dev/en/latest/index.html),
[Flask](https://flask.palletsprojects.com/) e 
[Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot),
 então é necessário instalá-los para rodar o bot.  

A biblioteca **secrets** exige headers do LDAP e OpenSSL. Para instalar no 
Debian/Linux:  

```bash
user@home:~/matebot$ sudo apt install python3-{openssl,ldap,dev} lib{ldap2,ssl,sasl2}-dev
```

Ritual de instalação:  

#### pipenv

O jeito mais fácil de todos é usar [pipenv](https://pipenv.pypa.io/), inclusive 
está incluso o Pipfile no repositório:  

```bash
user@home:~/matebot$ python3 -m ensurepip  
user@home:~/matebot$ python3 -m pip install --user --upgrade pip pipenv  
user@home:~/matebot$ pipenv install  
```

#### Outras formas

Quem não quiser usar pipenv pode usar virtualenvwrapper, virtualenv ou outro 
método de preferência se souber o que está fazendo. Um arquivo 
`requirements.txt` é mantido atualizado no repositório.  

```bash
user@home:~/matebot$ python3 -m ensurepip
user@home:~/matebot$ python3 -m pip install --user --upgrade pip
user@home:~/matebot$ python3 -m pip install --user -r requirements.txt
```

**TODO**_: Fazer instruções para usar sem pipenv_  

---

### Configurando

Criar o diretório *instance*:  

```bash
user@home:~/matebot$ mkdir instance
```

Renomear o arquivo `doc/default_config.py` para `instance/config.py`.  

```bash
user@home:~/matebot$ cp doc/default_config.py instance/config.py
```

Editar o arquivo de configuração, pelo menos adicionando tokens para o valor 
obtido através do [@BotFather](https://t.me/botfather).  

A parte da configuração que é necessário alterar se parece com isto:

```python
'matebot': {
  ## Obtenha um token com @BotFather no Telegram
  'token': "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
```

Onde **123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11** deve ser substituída com a 
token providenciada pelo BotFather.  

Uma forma alternativa de alterar este campo é diretamente na linha de comando 
usando sed:  

```bash
user@home:~/matebot$ TOKEN="654321:ZXC-VBN4321ghIkl-zyx57W2v1u123ew11"; sed -i 's/123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/'${TOKEN}'/g' instance/config.py
```

Alterar os demais campos de configuração de acordo com a necessidade, cada 
opção está comentada no arquivo de configuração de exemplo 
`doc/default_config.py`.  

**TODO**_: Documentar exemplos de uso do arquivo de configuração para um bot ou
vários bots_  

#### Flask / Quart

Para usar a versão com Flask (ou Quart), é necessário também renomear o arquivo 
`doc/default_env` para `.env`. Ou criar um arquivo `.env` com as variáveis 
**FLASK_APP** e **FLASK_ENV** (ou **QUART_APP** / **QUART_ENV**).  

#### Webhook

Para gerar certificados auto assinados com OpenSSL no diretório instance/:  

```bash
user@home:~/matebot/instance$ openssl req -newkey rsa:2048 -sha256 -nodes -keyout matebot.key -x509 -days 365 -out matebot.pem -subj "/C=BR/ST=Rio Grande do Sul/L=Porto Alegre/O=Matehackers/CN=localhost.localdomain"
```

Rodar proxy reverso na porta 8443 com pipenv:  

```bash
user@home:~/matebot$ pipenv run webhook
```

---

### Rodando

No diretório principal do *matebot*:  

#### pipenv

Para rodar com pipenv, assumindo que a configuração já está correta:  

```bash
user@home:~/matebot$ pipenv run matebot
```

Se tiver mais bots configurados, informar o nome da chave do token do arquivo 
de configuração:  

```bash
user@home:~/matebot$ pipenv run matebot production
```

O método anterior para usar Flask e python-telegram-bot:  

```bash
user@home:~/matebot$ pipenv run ptb
```

O método antigo pra usar telepot (não recomendado):  

```bash
user@home:~/matebot$ pipenv run telepot
```

#### Outros métodos

Quem estiver usando outra coisa que não seja pipenv, pode usar o script 
`app.py` que vai tentar encontrar os módulos e arquivos de configuração 
pertinentes. Alguns exemplos:  

```bash
user@home:~/matebot$ python3 start.py aiogram matebot
```

```bat
C:\Users\user\tg-matebot> Python start.py flask matebot
```

Para parar, enviar um sinal *KeyboardInterrupt* (**CTRL+C**).  

---

### Deploy / produção

#### Systemd

Exemplo de arquivo para usar com systemd:  

```systemd
[Unit]
Description=MateBot daemon
After=network.target nss-lookup.target

[Service]
Type=simple
ExecStart=/home/user/.local/bin/pipenv run matebot
WorkingDirectory=/home/user/matebot/
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Em um sistema Debian, este arquivo deveria estar em 
`${HOME}/.config/systemd/user/matebot.service`.  

Habilitando o serviço na inicialização do sistema e iniciando agora:  

```bash
user@home:~$ systemctl --user daemon-reload  
user@home:~$ systemctl --user enable matebot.service  
user@home:~$ systemctl --user -l start matebot.service  
```

Para ver se está funcionando:  

```bash
user@home:~$ systemctl --user -l status matebot.service  
```

Parar:  

```bash
user@home:~$ systemctl --user stop matebot.service  
```

Remover da inicialização:  

```bash
user@home:~$ systemctl --user disable matebot.service  
```

Reiniciar:  

```bash
user@home:~$ systemctl --user -l restart matebot.service  
```

Para o caso de usar systemd como root, o arquivo de configuração deve estar em 
`/lib/systemd/system/matebot.service`, e os comandos devem ser utilizados 
sem o `--user`, como por exemplo:  

```bash
root@home:/root# systemctl -l restart matebot.service  
```

Mas eu não recomendo esta abordagem.  

#### Crontab

Também é possível usar cron para verificar se o bot está no ar periodicamente:  

```bash
user@home:~$ crontab -e  
```

Adicione uma linha como por exemplo esta na crontab:  

```crontab
*/10 * * * * /usr/lib/systemctl --user is-active matebot.service || /usr/lib/systemctl --user restart matebot.service  
```

Isto vai verificar se o bot está no ar a cada 10 minutos, e reiniciar o serviço 
caso esteja fora do ar.  

#### Docker

Adicione seu token em `BOTFATHER_TOKEN` no arquivo `doc/default_env` e depois rode os comandos abaixo na raiz do projeto 

 ```bash
 docker build -t matebot -f Dockfile .
 docker run -d --name matebot matebot
 docker inspect matebot | grep IPAddress
 ```

Após esses comandos você terá o IP do seu container pegue esse IP e acesse via `CURL IP:5000`

#### Heroku / Python Anywhere

Existem usuária(o)s do bot que usam Heroku e Python Anywhere solicitando ajuda 
para configurar o robô nestes serviços. Eu nunca usei nada disto então preciso 
de ajuda para tal feito.  

---

Licença
---

Copyleft 2012-2020 Iuri Guilherme, 2017-2020 Matehackers, 2018-2019 Velivery, 
2019 Greatful, 2019-2020 Fábrica do Futuro  

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
