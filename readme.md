# Análise de Dados no PGD Petrvs

** dm_petrvs

O dm_petrvs é uma ferramenta de consulta à base de dados do PGD Petrvs com a finalidade de fornecer insumos para procedimentos de análise de dados.

A aplicação gera, em banco próprio (PosgreSQL), tabelas stage, dimensões, fato, além de tabelas de trabalho.

As tabelas stage e de dimensão compreendem:

* unidades
* usuarios
* planos_entregas
* entregas
* planos_trabalho
* trabalhos
* avaliacoes
* tempo

O, até então, único datamart (ft_desempenho) busca agregar os dados do que se interessa medir em um programa de gestão do desempenho: O desempenho.

O sistema, fazendo uso de tabelas de trabalho, permite que sejam definidos grupos de entregas a partir de palavras chaves, o que é útil para se agrupar entregas em temas de interesse do órgão. Isto é particularmente útil no estudo da dinâmica das entregas.

O sitema é "dockerizado" e está preparado para uma instalação local. Para a instalação, verifique o arquivo docker-compose.yaml e ajuste para o caso concreto. Usualmente, o que se precisa ajustar são as variáveis temporais e de acesso ao banco de dados do PGD Petrvs:

    DATA_INI: "2020-01-01"
    DATA_FIM: "2030-12-31"

    PETRVS_DB_PORT: "<a porta do banco de dados do seu tenant>"
    PETRVS_DB_DATABASE: "<o nome do banco de dados do seu tenant>"
    PETRVS_DB_SERVER: "<host.docker.internal deve ser usado na instalação local>"
    PETRVS_DB_USER: "<o usuario do banco de dados do seu tenant, pode ser o root, para facilitar>"
    PETRVS_DB_PWD: "<a senha do usuário acima>"

** IMPORTANTE: Após a instalação do sistema (subida dos contêineres), deve-se criar o banco de dados que o sistema irá utilizar, isto é feito via "flask db migrate", seguido por "flask db upgrade", no terminal (exec) do contêiner dm_petrvs. Problemas de migração costumam ser resolvidos simplesmente deletando as migrações antigas (pasta migrations/versions) e removendo a tabela alembic_version, no banco de dados, caso ela exista.

** pgadmim

No pacote, é instalada uma instância do pgadmin, que é útil caso se deseje acessar diretamente as tabelas do sistema (dm_petrvs).

Para o seu uso, alguma configuração manual é necessária.

Abra o pgadmin (localhost:5000) e adicione um novo servidor.

Na aba General, coloque um nome para o servidor (dm_petrvs, por exemplo).
A porta é 5432.
No nome do host, coloque o nome do contêiner onde está o banco do dm_petrvs: postgres.
O nome do banco é bd_dm_petrvs.
Usuário e senha: postgres/postgres.

** superset

Incorporado também segue uma aplicação de BI: Superset.

Abra o superset (localhost:8088) e faça a conexão com o banco de dados do dm_petrvs: Opção "Settings" >> "Database Connections" >> "+ Database". Escolha PostgreSQL. Em "Host", informe o nome do contêiner do banco do dm_petrvs: postgres, ou host.docker.internal. Em "Port", deixe 5432, "Database name" é bd_dm_petrvs, "Username" é postgres e "Senha" é postgres.

O Superset tem váarios dashbords de exemplo, o que dá uma ideia das suas potencialidades. Neste repositório GIT seguem também alguns dasboards que utilizam dados do dm_petrvs. Estão na pasta Dasboards.

Na opção "Dashboards" do Superset, no canto superior direito, há um ícone para importação de dashboards. Clique nele, selecione o arquivo desejado, caso solicite senha, informe a senha de acesso ao banco de dados (postgres). O Dasboard estará disponível para visualização.

Caso deseje as consultas SQL utilizadas, pode importá-las também. Estas estão na pasta Consultas SQL.