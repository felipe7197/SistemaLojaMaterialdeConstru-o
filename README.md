# Sistema Loja de Material de Construção

Sistema desktop desenvolvido em Python para apoiar a operação de uma loja de materiais de construção. Pela estrutura mostrada no repositório, o sistema reúne módulos de login, painel principal, vendas, estoque, fornecedores, funcionários, faturamento e banco de dados local em SQLite. [1]

## Visão geral

O objetivo do sistema é centralizar rotinas operacionais em uma única aplicação, facilitando o controle de cadastros, movimentações e consultas administrativas. A organização dos arquivos sugere uma arquitetura modular, em que cada parte do negócio foi separada em arquivos específicos para melhorar manutenção e navegação interna. [1]

## O que o sistema faz

Com base nos arquivos visíveis no projeto, o sistema parece oferecer as seguintes áreas funcionais: [1]

- Autenticação de acesso por meio do módulo `login.py`. [1]
- Acesso a um painel principal através do módulo `dashboard.py`. [1]
- Controle de vendas com apoio do arquivo `sales.py`. [1]
- Controle de estoque usando o módulo `stock.py`. [1]
- Cadastro e acompanhamento de fornecedores em `supplier.py`. [1]
- Cadastro e controle de funcionários no módulo `employeer.py`. [1]
- Rotinas de faturamento tratadas em `billing.py`. [1]
- Persistência de dados em banco SQLite por meio do arquivo `tbs.db` e da configuração definida em `db_config.py`. [1]

## Estrutura principal

A imagem do repositório mostra os arquivos centrais e ajuda a entender como o sistema foi dividido. A tabela abaixo resume os componentes mais importantes visíveis no projeto. [1]

| Arquivo ou pasta | Papel no sistema |
|---|---|
| `main.py` | Arquivo principal para iniciar a aplicação. [1] |
| `login.py` | Controle de autenticação e entrada do usuário. [1] |
| `dashboard.py` | Painel inicial com acesso às funções principais. [1] |
| `sales.py` | Rotinas relacionadas a vendas. [1] |
| `stock.py` | Controle e consulta de estoque. [1] |
| `supplier.py` | Gestão de fornecedores. [1] |
| `employeer.py` | Gestão de funcionários ou colaboradores. [1] |
| `billing.py` | Emissão ou controle de faturamento. [1] |
| `create_db.py` | Criação ou preparação do banco de dados. [1] |
| `db_config.py` | Configuração de acesso ao banco. [1] |
| `tbs.db` | Banco SQLite usado pelo sistema. [1] |
| `imagens/` | Recursos visuais da interface. [1] |
| `dist/` e `build/` | Estruturas ligadas à geração de executável. [1] |
| `SistemaLoja.spec` | Arquivo de configuração do empacotamento. [1] |

## Como o sistema funciona

O fluxo esperado começa pela abertura da aplicação principal, seguida da autenticação do usuário e do acesso ao painel central. A partir desse painel, o usuário escolhe o módulo desejado para executar tarefas como registrar vendas, consultar estoque, administrar fornecedores ou manter informações de funcionários. [1]

De forma prática, o funcionamento pode ser entendido assim:

1. O usuário abre o sistema.
2. Realiza o login, quando essa etapa estiver habilitada.
3. Entra no painel principal.
4. Seleciona o módulo de trabalho conforme a necessidade do momento.
5. Registra, consulta ou atualiza informações no banco de dados local. [1]

## Como utilizar

### Início da aplicação

O arquivo `main.py` aparece como ponto principal do projeto, então ele tende a ser o responsável por abrir o sistema. Em uma instalação com Python configurado, a execução normalmente acontece com o seguinte comando: [1]

```bash
python main.py
```

Se o sistema ainda não tiver o banco configurado ou se for uma primeira execução em ambiente novo, o arquivo `create_db.py` pode ser usado para preparar a base de dados inicial. [1]

```bash
python create_db.py
```

### Acesso ao sistema

Depois de iniciar o programa, a etapa esperada é a autenticação na tela de login. Essa entrada serve para controlar quem pode acessar os módulos internos do sistema. [1]

### Uso do painel principal

Após o login, o painel principal deve concentrar os atalhos para as áreas mais importantes da aplicação. Esse tipo de organização ajuda o usuário a localizar rapidamente as funções operacionais do dia a dia. [1]

### Vendas

O módulo de vendas tende a concentrar lançamentos comerciais, registro de itens vendidos e atualização das movimentações relacionadas ao atendimento. Como existe um arquivo `sales.py`, essa parte provavelmente é dedicada à operação comercial da loja. [1]

### Estoque

O módulo de estoque deve permitir acompanhar produtos disponíveis, entradas, saídas e consulta de itens. Em um sistema para loja de materiais de construção, esse controle é importante para evitar falta de mercadoria e divergências de saldo. [1]

### Fornecedores

A presença do arquivo `supplier.py` indica um espaço próprio para cadastrar e gerenciar fornecedores. Isso ajuda a organizar origem dos produtos, contatos comerciais e possíveis consultas administrativas. [1]

### Funcionários

O arquivo `employeer.py` sugere um módulo de cadastro e acompanhamento de funcionários ou colaboradores. Esse espaço pode reunir informações internas importantes para controle operacional. [1]

### Faturamento

Com o módulo `billing.py`, o sistema aparenta possuir uma área voltada para rotinas de faturamento. Dependendo da implementação, isso pode envolver geração de registros financeiros, totalizações e acompanhamento de movimentações ligadas às vendas. [1]

## Banco de dados

O sistema utiliza o arquivo `tbs.db`, o que indica uso de SQLite como base local. Esse modelo é comum em sistemas desktop porque simplifica a instalação, reduz dependências externas e mantém os dados em um único arquivo. [1]

Cuidados importantes com a base de dados:

- Fazer cópias de segurança periódicas do arquivo `tbs.db`. [1]
- Evitar apagar ou substituir o banco sem antes guardar uma cópia segura.
- Conferir em `db_config.py` se o caminho do banco está correto quando o sistema for movido para outra máquina. [1]
- Testar alterações em ambiente separado antes de usar o sistema com dados reais.

## Executável do sistema

As pastas `build/`, `dist/` e o arquivo `SistemaLoja.spec` indicam que o projeto já foi preparado para gerar uma versão executável. Isso é útil para disponibilizar o sistema para usuários que não trabalham diretamente com código-fonte ou ambiente Python. [1]

Quando um executável estiver pronto, a tendência é que o usuário final possa abrir o sistema diretamente por ele, sem precisar rodar comandos manuais. A localização final normalmente fica na pasta `dist/`, de acordo com a estrutura visível no repositório. [1]

## Perfil de uso

Esse sistema parece ter sido pensado para uso administrativo e operacional em loja ou escritório, com foco em organização interna. A separação dos módulos mostra preocupação em dividir as responsabilidades do negócio e facilitar o trabalho diário de quem cadastra, consulta e atualiza dados. [1]

## Boas práticas de utilização

Para melhor aproveitamento do sistema, algumas orientações são úteis:

- Manter o banco de dados salvo em local seguro. [1]
- Registrar informações com padronização, especialmente nomes de produtos, fornecedores e funcionários.
- Evitar fechamento brusco da aplicação durante gravação de dados.
- Testar novas versões antes de colocar o sistema em uso contínuo.
- Organizar a pasta `imagens/` e outros recursos para não quebrar a interface, já que esse diretório aparece como parte da estrutura do projeto. [1]

## Limitações e pontos de atenção

Como a análise foi feita a partir da estrutura mostrada no repositório, algumas funcionalidades exatas dependem da implementação interna de cada arquivo. Ainda assim, a divisão do projeto já permite compreender com boa segurança o propósito geral do sistema e a forma como o usuário deve interagir com ele. [1]

## Sugestões para melhorar a experiência do usuário

Alguns complementos podem deixar a documentação do sistema ainda mais útil:

- Adicionar imagens reais das telas principais.
- Descrever usuários padrão e níveis de acesso, caso existam.
- Explicar os campos mais importantes de cada cadastro.
- Incluir exemplos de uso para venda, estoque e fornecedores.
- Criar uma seção de dúvidas frequentes com erros comuns e soluções rápidas.
