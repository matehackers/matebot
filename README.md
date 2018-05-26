Bot de Telegram para Matehackers
===

O que
---

Este é um [bot de Telegram](https://telegram.org/faq#bots) escrito em [Python](https://python.org) para o hackerspace [Matehackers](https://matehackers.org).  
Este é o código fonte do bot funcionando em [@Mate_obot](https://telegram.me/mate_obot).  

Este bot pode ser extendido com o uso de plugins, inspirado no supybot.  

Uso
---

Chame o bot em [@mate_obot](https://t.me/mate_obot) para ver a lista de comandos.  

Se o bot estivesse em ação, ele estaria no [canal do Matehackers no Telegram](https://t.me/matehackers).  

Quem tiver qualquer dúvida pode entrar no [grupo do Matehackers no Telegram](https://t.me/matehackerspoa). Todo mundo lá também tem dúvidas, tu vai te sentir em casa.  

### Comandos

Atualmente o bot tem os seguintes comandos:  

#### /start

Não faz nada.  

**Exemplo**: `/start`  

#### /help

Não faz nada.  

**Exemplo**: `/help`  

#### /feedback

Envia mensagem para os desenvolvedores do bot.  

**Exemplo**: `/feedback Esse bot não funciona!`  

#### /hash

Calcula o hash de um texto. O texto pode ser qualquer coisa, observado o limite de tamanho de mensagem do telegram.  

**Exemplo**: `/hash Mensagem secreta`  

#### /qr

Cria uma imagem png com um QR code representando o texto que foi enviado. O texto pode ser qualquer coisa.  

**Exemplo**: `/qr https://matehackers.org`

Fork
---

Se você quiser usar o código deste bot pra fazer o seu próprio, você deve:  

### Entender e usar a licença GPL v3

Para mais informações, veja o arquivo [LICENSE.md](./LICENSE.md).  

### Aprender a usar git

...e incidentalmente, Github - que é outra coisa completamente diferente de git.  

Para mexer no código agora mesmo no Linux:  

```bash
$ git clone -b stable https://github.com/matehackers/tg-matebot.git
$ cd tg-matebot
```

### Dependências

Este bot foi testado com Python 3.4  
Se você não tiver Python, [instale!](https://www.python.org/downloads/)  

Estamos usando [Telepot](https://github.com/nickoala/telepot), então é necessário instalá-lo para rodar o bot.  
Tente `pip3 install --user telepot` ou `python3 -m pip install --user telepot`. Ou melhor, `pip3 install -r requirements.txt` para instalar todas as dependências dos plugins. Se este comando não funcionar, [instale pip](https://pip.pypa.io).  

### Configurando

No diretório *config*:  
Renomeie o arquivo `matebot.cfg.example` para `.matebot.cfg`. Sem este arquivo, o bot não vai funcionar.  
Edite o arquivo, alterando o valor de `token` na seção `[botfather]` para o valor obtido através do [@BotFather](https://telegram.me/botfather).  
Altere os demais campos de configuração de acordo com a necessidade.  

### Rodando

No diretório principal do *matebot*:  
Se for UNIX, rode com `./start.py`  
Em qualquer plataforma, deveria funcionar com `python3 start.py`  
Para parar, envie um sinal *KeyboardInterrupt* (no Linux, CTRL+C).  

### Administração

Envie uma mensagem para o bot e preste atenção no console para descobrir qual é o seu id do telegram.  
Deveria aparecer algo parecido com isto:  

    [2017-05-09 13:37:26.113188] RCV: Received "hi" from 123456789

Onde `123456789` é o seu telegram id. Coloque este número no arquivo de configuração, na seção `[admin]`, item `id`. O arquivo é `config/.matebot.cfg` conforme explicado acima, veja **Configurando**.  
Isto possibilita usar comandos especificamente para administração do bot.  

Além disto, é possível configurar um id de grupo de administração, que é parecido com `-123456789`. Este grupo é para onde o bot envia informações de depuração (debug) e onde o comando `/feedback` envia feedback.  

### Systemd

Exemplo de arquivo para usar com systemd:  

```systemd
[Unit]
Description=tg-matebot daemon
After=network.target nss-lookup.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/user/tg-matebot/start.py
WorkingDirectory=/home/user/tg-matebot/
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Em um sistema Debian, este arquivo deveria estar em `/lib/systemd/system/tg-matebot.service`, ou `${HOME}/.config/systemd/user/tg-matebot.service`.  

Habilitando o serviço na inicialização do sistema e iniciando agora:  

```bash
# systemctl daemon-reload
# systemctl enable tg-matebot.service
# systemctl -l start tg-matebot.service
```

Para ver se está funcionando:  

```bash
# systemctl -l status tg-matebot.service
```

Parar:  

```bash
# systemctl stop tg-matebot.service
```

Reiniciar:  

```bash
# systemctl -l restart tg-matebot.service
```

Para o caso de usar systemd como usuário, o arquivo de configuração deve estar em `${HOME}/.config/systemd/user/tg-matebot.service`, e os comandos devem ser precedidos de `--user`, como por exemplo:  

```bash
# systemctl --user -l restart tg-matebot.service
```

#### Crontab

Também é possível usar cron para verificar se o bot está no ar periodicamente:  

```bash
# crontab -e
```

Adicione uma linha como por exemplo esta na crontab:  

```crontab
*/10 * * * * /usr/lib/systemctl --user is-active tg-matebot.service || /usr/lib/systemctl --user start tg-matebot.service
```

Isto vai verificar se o bot está no ar a cada 10 minutos, e iniciar o serviço caso esteja fora do ar.  

Roadmap
---

### TODO

- [x] Traduzir este README ~~~(pedi ajuda nos grupos de telegram e ninguém fez merda nenhuma. grupo de telegram é que nem grupo de feisse e uáts - só tem sofista e gente fazendo nada!)~~~  
- [ ] Usar dicionários em todos os retornos de funções  
- [ ] Melhorar o empacotamento dos plugins  
- [ ] Tratar as exceções corretamente, principalmente as informativas

Licença
---

Copyleft 2017-2018 Matehackers, Desobediente Civil  

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

### Informações

Este bot aproveita o trabalho feito no [tg-cryptoforexbot](https://github.com/desci/tg-cryptoforexbot) e é laboratório para melhorar o código de outro bot, a [Paloma](https://notabug.org/desci/Paloma). Assim como este código é reaproveitado em outro bot, o VeliveryBot, que por sua vez contribui com código e melhorias para este. Viva o software livre.  

