Vegga
===

O que
---

Este é um [bot de Telegram](https://telegram.org/faq#bots) baseado em plugins escrito em [Python](https://python.org) para o [Velivery](https://velivery.com.br).  
Clonado do bot original [MateBot](https://github.com/matehackers/tg-matebot) para o hackerspace [Matehackers](https://matehackers.org).  
Matebot por sua vez é clonado de [CryptoForexBot](https://github.com/desci/tg-cryptoforexbot).  
Todos estes bots são inspirados na [Paloma](https://notabug.org/desci/Paloma), originalmente um bot de IRC inspirado na [lalenia](http://wiki.nosdigitais.teia.org.br/Lalenia), que é um [supybot](https://github.com/Supybot). Viva o software livre.  

Uso
---

Este bot serve para automatizar determinadas áreas no trabalho do Velivery. Somente funcionária(o)s autorizada(o)s têm ou deveriam ter acesso.  

### Comandos

Atualmente o bot tem os seguintes comandos:  

#### /ajuda

Exibe os atuais comandos da Vegga. Atualmente quase todos exigem autenticação automática através do controle de acesso por id de usuário do telegram.  

**Exemplo**: `/ajuda`  

#### /feedback

Envia mensagem para os desenvolvedores do bot.  

**Exemplo**: `/feedback Esse bot não funciona!`  

#### /qr

Cria uma imagem png com um QR code representando o texto que foi enviado. O texto pode ser qualquer coisa.  

**Exemplo**: `/qr https://matehackers.org`

Fork
---

Se você quiser usar o código deste bot pra fazer o seu próprio, você deve:  

### Entender e usar a licença GPL v3

Para mais informações, veja o arquivo [LICENSE.md](./LICENSE.md).  

### Aprender a usar git

...e incidentalmente, Notabug - que é outra coisa completamente diferente de git.  

Para mexer no código agora mesmo no Linux:  

```bash
$ git clone -b stable https://notabug.org/velivery/vegga.git
$ cd vegga
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

    [2018-08-24 11:36:49.201162] [INFO] O nosso token do @BotFather é '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11', os ids de usuária(o)s administradora(e)s são '[123456789]' e os ids dos grupos administradores são '[-987654321]'. O nome de usuário da(o) administrador(a) é '@desobedientecivil'.

Onde `123456789` é o seu telegram id. Coloque este número no arquivo de configuração, na seção `[admin]`, item `id`. O arquivo é `config/.matebot.cfg` conforme explicado acima, veja **Configurando**.  
Isto possibilita usar comandos especificamente para administração do bot.  

Além disto, é possível configurar um id de grupo de administração, que é parecido com `-987654321`. Este grupo é para onde o bot envia informações de depuração (debug) e onde o comando `/feedback` envia feedback.  

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
- [x] Usar dicionários em todos os retornos de funções  
- [x] Melhorar o empacotamento dos plugins  
- [ ] Tratar as exceções corretamente, principalmente as informativas  
  - [x] Exceções informativas para quem está tentando instalar o bot do zero suficientemente tratadas e suficientemente informativas com commit 367613a  

Licença
---

Copyleft 2016-2018 Desobediente Civil, 2017-2018 Matehackers, 2018 Velivery  

**Este programa é distribuído na esperança de que possa ser útil,**  
**mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO**  
**a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a**  
**Licença Pública Geral GNU para mais detalhes.**  

**Você deve ter recebido uma cópia da Licença Pública Geral GNU junto**  
**com este programa (veja o arquivo LICENSE.md).**  
**Se não, veja <http://www.gnu.org/licenses/>.**  

