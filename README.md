# Watermarked Docs

Documentos com marca d'água enviados por e-mail com chamada via telegram.

Este projeto facilita o envio de documentos com marca d'água por meio de um bot do Telegram, adicionando proteção e
rastreabilidade às informações compartilhadas. Ele permite identificar a fonte de qualquer vazamento digital, trazendo
segurança adicional ao processo.

## Tabela de Conteúdo

1. [Visão Geral](#visão-geral)
2. [Como Funciona](#como-funciona)
    1. [Bot do Telegram](#bot-do-telegram)
    2. [Configuração do E-mail](#configuração-do-e-mail)
    3. [Arquivo pessoas.json](#arquivo-pessoasjson)
3. [Configuração de Acesso ao Bot](#configuração-de-acesso-ao-bot)
4. [Instalação e Execução](#Execução)

## Visão Geral

Logo, se algum documento for extraviado digitalmente você terá meios de identificar qual foi a empresa responsável pelo
vazamento e acionar a justiça.

Para iniciar a interação com o bot, adicione-o aos seus contatos, abra uma conversa com o bot e digite: `/fotos`. Então
as seguintes perguntas que serão feitas:

* Escolha a pessoa:
* Você deseja enviar também os documentos do pai, da mãe, ou de nenhum?
* Qual o endereço de e-mail do destinatário da mensagem?
* Qual o local?

Com base nessas perguntas, o bot irá gerar uma ou várias imagens conforme configuração com marcas d'água repetidas
contendo o `local - data de envio`, por exemplo: `hospital XYZ 16/04/2025 19:55`. O bot então vai anexar todas essas
imagens em um e-mail e enviar para o endereço de e-mail informado.

## Como funciona

### Bot do telegram

Antes de qualquer coisa você precisará de um token do telegram para que o bot esteja disponível e ouvindo as mensagens.
Para criar um bot e gerar o token leia mais na [Página sobre bots do telegram](https://core.telegram.org/bots).

Adicione o token de acesso ao telegram no arquivo `.env`, conforme exemplo disponibilizado.

### Configuração do E-mail

Para configurar as variáveis de ambiente referentes ao envio de e-mail usando o gmail, você deverá criar uma
`chave de aplicativo`, como explicado
em: [Inicie sessão com palavras-passe de apps](https://support.google.com/mail/answer/185833?hl=pt)

Lembrando que você pode usar quaisquer outros servidores de e-mail que trabalhem com o protocolo `SMTP`.

### Arquivo pessoas.json

Você deverá criar um arquivo chamado `pessoas.json`, na raíz do projeto contendo uma lista de pessoas, conforme exemplo
abaixo:

```JSON
[
  {
    "nome": "John Smith",
    "indice": "John",
    "documentos": [
      "john_id.jpg"
    ],
    "is_parent": true
  },
  {
    "nome": "John Smith",
    "indice": "John",
    "documentos": [
      "john_passport.jpg",
      "john_id.jpg"
    ]
  },
  {
    "nome": "Emily Johnson",
    "indice": "Emily",
    "documentos": [
      "emily_passport.jpg",
      "emily_id.jpg",
      "emily_ssn.jpg"
    ]
  },
  {
    "nome": "Michael Brown",
    "indice": "Michael",
    "documentos": [
      "michael_passport.jpg",
      "michael_id.jpg"
    ]
  }
]
```

Abaixo uma breve descrição das variáveis:

| Variável       | Descrição                                                                          |
|----------------|------------------------------------------------------------------------------------|
| **nome**       | O nome completo da pessoa, usado no título dos e-mails.                            |
| **indice**     | Nome curto exibido nas conversas com o bot.                                        |
| **documentos** | Lista de nomes de arquivos de imagens localizadas no diretório `./documentos`.     |
| **is_parent**  | Indica se a pessoa é pai/mãe. Os responsáveis aparecem na segunda pergunta do bot. |

> Observação:
>
> No exemplo acima John Smith aparece duas vezes, uma com a flag is_parent = True e outra com a flag False. Isso fará
> que o nome dele apareça nas duas perguntas, mas com uma lista de documentos diferentes.
>
> Na primeira pergunta do bot, só aprecerão os nomes das pessoas com a flag is_parent = False
>
> Na segunda pergunta do bot, só aparecerão os nomes das pessoas com a flag True.

### Configuração de Acesso ao Bot

Toda vez que há uma interação com o bot, é impresso no console da aplicação o usuário que fez a interação.

Você deverá preencher o campo `PERMITED_USERS` com os `id` dos usuários que você quer permitir o acesso. Se você quiser
permitir mais de um usuário, você deverá usar uma vírgula para separar os valores (não use espaços nem antes, nem depois
de cada virgula).

> Dica
>
> Começe a utilizar seu bot sem informar os usuários permitidos, anote os IDs dos usuários que você deseja permitir (ver
> o log) e depois reinicie o serviço com a lista de usuários permitidos preenchida.

### Execução

Para que o bot funcione você precisa rodar o script `telegram_bot.py`, simples assim. Lembrando que não é possível dois
ou mais bots rodarem ao mesmo tempo.

