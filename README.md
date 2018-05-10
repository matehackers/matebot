Bot de Telegram para Velivery
===

O que
---

Este é um [bot de Telegram](https://telegram.org/faq#bots) escrito em [Python](https://python.org) para o [Velivery](http://velivery.com.br).  
Clonado do bot original para o hackerspace [Matehackers](https://matehackers.org) funcionando em [@Mate_obot](https://telegram.me/mate_obot).  

Uso
---

Este bot serve para automatizar determinadas áreas no trabalho do Velivery. Somente funcionária(o)s autorizada(o)s têm ou deveriam ter acesso.  

---

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

Este bot foi testado com Python 2.7.12  
Se você não tiver Python, [instale!](https://www.python.org/downloads/)  

Estamos usando [Telepot](https://github.com/nickoala/telepot), então é necessário instalá-lo para rodar o bot.  
Tente `pip install telepot`. Ou melhor, `pip install -r requirements.txt` para instalar todas as dependências.  

### Configurando

No diretório *config*:  
Renomeie o arquivo `matebot.cfg.example` para `matebot.cfg`.  
Edite o arquivo, alterando o valor de `token` na seção `[botfather]` para o valor obtido através do [@BotFather](https://telegram.me/botfather).  

### Rodando

No diretório principal do *matebot*:  
Se for UNIX, rode com `./start.py`  
Em qualquer plataforma, deveria funcionar `python start.py`  
Para parar, envie um sinal *KeyboardInterrupt* (no Linux, CTRL+C).  

### Administração

If you don't know what is your telegram id, make sure you leave the debugging logs on and send a private message to your bot.  
You should see something like this:  

    [2017-05-09 13:37:26.113188] RCV: Received "hi" from 123456789

Where `123456789` is your telegram id. Make sure you put that in the configuration file, in the `[admin]` section - the file is `cryptoforexbot/cryptoforexbot.cfg` as explained above, see **Configuring**.  

Also, you may configure a group admin id, which looks like `-123456789`. This will help with debug logging and it's where the user feedback is sent.

### Systemd

If you are running the bot on a Linux server (or other systemd capable), use the following *systemd* service file for a daemon:

```systemd
[Unit]
Description=tg-matebot daemon
After=network.target nss-lookup.target

[Service]
Type=simple
ExecStart=/usr/bin/python2.7 /home/user/tg-matebot/start.py
WorkingDirectory=/home/user/tg-matebot/
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

On a Debian system, this should reside at `/lib/systemd/system/tg-matebot.service`.

Enable the service and start:

```bash
# systemctl daemon-reload
# systemctl enable tg-matebot.service
# systemctl -l start tg-matebot.service
```

To see if it's working:

```bash
# systemctl -l status tg-matebot.service
```

To stop:

```bash
# systemctl stop tg-matebot.service
```

Or restart:

```bash
# systemctl -l restart tg-matebot.service
```

#### Crontab

You can also put a watchdog cronjob to make sure it will restart on failure:

```bash
# crontab -e
```

Add a line like this in the crontab:

```crontab
*/10 * * * * /usr/lib/systemctl is-active tg-matebot.service || /usr/lib/systemctl start tg-matebot.service
```

This would check every 10 minutes if the bot is running and start it in case it wasn't.

Roadmap
---

### TODO

- [ ] Traduzir este README

Disclaimer
---

**This bot is provided in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Use at your own risk.**  

Licença
---

Copyleft 2016-2018 Desobediente Civil, 2017-2018 Matehackers, 2018 Velivery  

This is GPL software. Which basically means that if you modify the source code, you need to distribute the modified version WITH the modified source code and with the same license.  
See the file *LICENSE.md* which should be distributed with this software.  

### Informações

Este bot aproveita o trabalho feito no [tg-cryptoforexbot](https://github.com/desci/tg-cryptoforexbot), no [tg-matebot](https://github.com/matehackers/tg-matebot), é laboratório para melhorar o código de outro bot, a [Paloma](https://notabug.org/desci/Paloma).

