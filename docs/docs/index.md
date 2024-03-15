# Documentação ST-CAFS

## Início

Esta documentação fornece uma visão geral do sistema ST-CAFS e orientações sobre como configurar, executar e estender suas funcionalidades.

### Detalhes da Arquitetura e Integrações

* Implantação em [Python 3](https://www.python.org).
* Foi feito uso do Framework [Django 4.2.8](https://www.djangoproject.com/).
* O banco de dados utilizado foi o [PostgreSQL](https://www.postgresql.org/), acesse o [diagrama de entidades e relacionamento(DER)](https://drive.google.com/file/d/1XSpE-rLkoXuwUgNRMDcwU5YNg_XaNQrS/view) para uma visualização do modelo.
* As bibliotecas utilizadas pelo projeto estão presentes no arquivo requirements.txt na raiz do projeto.

### Estrutura do projeto

Descrição da estrutura de diretórios do projeto e suas finalidades:

    setorT/                     # Diretório do projeto
        backups/                # Diretório de armazenamento dos backups
        docs/                   # Diretório da documentação
        setorT/                 # Diretório raiz do projeto Django
            settings.py
            urls.py
        sistema_gerenciamento/  # Diretório do app 
            migrations/         # Diretório de armazenamento das migrações do banco de dados
            templates/          # Diretório de armazenamento dos templates do projeto
            admin.py
            forms.py
            models.py
            urls.py
            views.py
        staticfiles/            # Diretório dos arquivos estáticos
        media/                  # Diretório dos arquivos de mídia
        backup.sh               # script de backup
        docker-compose.yml      # Arquivo de configuração do compose
        Dockerfile              
        manage.py
        nginx.conf              # Arquivo de configuração do nginx
        README.md
        requirements.txt

## Execução do Código

Para a execução do código é necessário realizar algumas configurações:

1. **Configuração do Banco de Dados**

    Configure o banco de dados no arquivo `settings.py` na raiz do projeto. 

2. **Docker-Compose**

    O projeto está configurado para execução com o docker-compose, onde algumas variáveis de ambiente e dependências já estão configuradas no arquivo `docker-compose.yml`.

3. **Rodar Migrações**

    Execute as migrações do Django com os seguintes comandos:

    - `docker-compose run web python manage.py makemigrations`

    - `docker-compose run web python manage.py migrate`

4. **Rodar o Projeto**

    Inicie o projeto com o seguinte comando:

    - Para rodar com os logs ativos use: `docker-compose up`

    - Para rodar sem os logs use: `docker-compose up -d`

5. **Backup do banco de dados**

    Configure o crontab para executar o script de backup em um horário determinado, caso queira realizar um backup manual navegue até a pasta do projeto e utilize o seguinte comando:

    - `./backup.sh`

    Para realizar a restauração do banco de dados utilize o seguinte comando:

     - `docker exec -i db psql -U setorT setorT < /caminho/para/o/arquivo/de/backup.sql`

## App - sistema_gerenciamento

Este é o app que fornece as principais funcionalidades referentes ao gerenciamento do sistema.

### Models

O aplicativo `sistema_gerenciamento` possui os seguintes modelos:

- `Veiculo`: Model responsável pelos veículos.
- `Manutencao`: Model responsável pelas manutenções.
- `Checklist`: Model responsável pelos checklists.
- `Motorista`: Model responsável pelos motoristas.
- `Rota`: Model responsável pelas rotas.
- `Combustivel`: Model responsável pelos abastecimentos.
- `Demanda`: Model responsável pelas demandas.
- `Viagem`: Model responsável pelas viagens.

### Views

As views do aplicativo sistema_gerenciamento são responsáveis por processar as requisições do usuário e retornar as respostas apropriadas, Aqui estão as views do app:

- `cadastro`: View responsável pelo cadastro de usuários.
- `user_login`: View responsável pelo login dos usuários.
- `user_logout`: View responsável pelo logout dos usuários.
- `home`: View responsável por redirecionar para a página home do sistema.
- `veiculos`: View responsável por listar e gerenciar veículos.
- `cadastrar_veiculos`: View responsável por cadastrar novos veículos.
- `editar_veiculo`: View responsável por editar veículos existentes.
- `deletar_veiculo`: View responsável por deletar veículos existentes.
- `manutencao`: View responsável por listar e gerenciar manutenções.
- `cadastrar_manutencao`: View responsável por cadastrar novas manutenções.
- `view_comprovante`: View responsável por exibir o comprovante de uma manutenção.
- `manutencoes_veiculo`: View responsável por listar manutenções de um veículo específico.
- `editar_manutencao`: View responsável por editar manutenções existentes.
- `deletar_manutencao`: View responsável por deletar manutenções existentes.
- `checklists`: View responsável por listar e gerenciar checklists.
- `cadastrar_checklist`: View responsável por cadastrar novos checklists.
- `view_comprovante_checklist`: View responsável por exibir o comprovante de um checklist.
- `editar_checklist`: View responsável por editar checklists existentes.
- `deletar_checklist`: View responsável por deletar checklists existentes.
- `motoristas`: View responsável por listar e gerenciar motoristas.
- `cadastrar_motorista`: View responsável por cadastrar novos motoristas.
- `visualizar_documentos`: View responsável por exibir os documentos de um motorista.
- `editar_motorista`: View responsável por editar motoristas existentes.
- `deletar_motorista`: View responsável por deletar motoristas existentes.
- `rotas`: View responsável por listar e gerenciar rotas.
- `cadastrar_rota`: View responsável por cadastrar novas rotas.
- `editar_rota`: View responsável por editar rotas existentes.
- `deletar_rota`: View responsável por deletar rotas existentes.
- `combustivel`: View responsável por listar e gerenciar abastecimentos de combustível.
- `cadastrar_abastecimento`: View responsável por cadastrar novos abastecimentos.
- `view_comprovante_abastecimento`: View responsável por exibir o comprovante de um abastecimento.
- `editar_abastecimento`: View responsável por editar abastecimentos existentes.
- `deletar_abastecimento`: View responsável por deletar abastecimentos existentes.
- `demandas`: View responsável por listar e gerenciar demandas de transporte.
- `cadastrar_demanda`: View responsável por cadastrar novas demandas.
- `editar_demanda`: View responsável por editar demandas existentes.
- `deletar_demanda`: View responsável por deletar demandas existentes.
- `viagens`: View responsável por listar e gerenciar viagens.
- `cadastrar_viagem`: View responsável por cadastrar novas viagens.
- `editar_viagem`: View responsável por editar viagens existentes.
- `deletar_viagem`: View responsável por deletar viagens existentes.

### Forms

Aqui estão os formulários definidos no projeto:

### CadastroForm

- **Campos:**
  - `username`: Campo para o nome de usuário.
  - `email`: Campo para o endereço de email.
  - `password1`: Campo para a senha.
  - `password2`: Campo para confirmar a senha.

### LoginForm

- **Campos:**
  - `username`: Campo para o nome de usuário.
  - `password`: Campo para a senha.

### VeiculoForm

- **Campos:**
  - `modelo`: Modelo do veículo.
  - `fabricante`: Fabricante do veículo.
  - `ano`: Ano do veículo.
  - `placa`: Placa do veículo.
  - `data_cadastro`: Data de cadastro do veículo.
  - `estado_funcionamento`: Estado de funcionamento do veículo.

### ManutencaoForm

- **Campos:**
  - `veiculo`: Veículo relacionado à manutenção.
  - `data`: Data da manutenção.
  - `descricao_manutencao`: Descrição da manutenção.
  - `comprovante_manutencao`: Comprovante da manutenção.

### ChecklistForm

- **Campos:**
  - `veiculo`: Veículo relacionado ao checklist.
  - `data`: Data do checklist.
  - `comprovante_checklist`: Comprovante do checklist.

### MotoristasForm

- **Campos:**
  - `nome`: Nome do motorista.
  - `telefone`: Telefone do motorista.
  - `data_cadastro`: Data de cadastro do motorista.
  - `documentos`: Documentos do motorista.

### RotaForm

- **Campos:**
  - `nome`: Nome da rota.
  - `turno`: Turno da rota.
  - `horario_saida`: Horário de saída da rota.
  - `horario_retorno`: Horário de retorno da rota.
  - `motorista`: Motorista associado à rota.
  - `veiculo`: Veículo associado à rota.
  - `paradas`: Paradas da rota.

### CombustivelForm

- **Campos:**
  - `veiculo`: Veículo associado ao abastecimento.
  - `data_cadastro`: Data do abastecimento.
  - `quantidade_abastecida`: Quantidade abastecida.
  - `custo`: Custo do abastecimento.
  - `comprovante_abastecimento`: Comprovante do abastecimento.

### DemandaForm

- **Campos:**
  - `veiculo`: Veículo associado à demanda.
  - `motorista`: Motorista associado à demanda.
  - `data`: Data da demanda.
  - `horario_saida`: Horário de saída da demanda.
  - `horario_retorno`: Horário de retorno da demanda.
  - `descricao`: Descrição da demanda.

### ViagemForm

- **Campos:**
  - `destino`: Destino da viagem.
  - `veiculo`: Veículo associado à viagem.
  - `motorista`: Motorista associado à viagem.
  - `solicitante`: Solicitante da viagem.
  - `data_saida`: Data de saída da viagem.
  - `data_retorno`: Data de retorno da viagem.
  - `descricao`: Motivo da viagem.

### URLs

A seguir estão as URLs mapeadas para as views correspondentes:

- `cadastro`: View responsável pelo cadastro de usuários.
- `user_login`: View responsável pelo login dos usuários.
- `user_logout`: View responsável pelo logout dos usuários.
- `home`: View responsável por redirecionar para a página home do sistema. 

### Recuperação de Senha

- `auth/password_reset/`: View para solicitação de redefinição de senha.
- `auth/password_reset/done/`: View exibida após a submissão bem-sucedida do formulário de redefinição de senha.
- `auth/reset/<uidb64>/<token>/`: View para a página de confirmação de redefinição de senha.
- `auth/reset/done/`: View exibida após a redefinição de senha ser concluída com sucesso.

### Veículos

- `home/veiculos/`: View para listar os veículos.
- `home/veiculos/cadastrar_veiculos`: View para cadastrar novos veículos.
- `home/veiculos/editar_veiculo/<int:veiculo_id>`: View para editar um veículo existente.
- `home/veiculos/deletar_veiculo/<int:veiculo_id>`: View para deletar um veículo existente.

### Manutenções

- `home/veiculos/manutencao`: View para listar as manutenções.
- `home/veiculos/<int:veiculo_id>/manutencoes/`: View para listar as manutenções de um veículo específico.
- `home/veiculos/manutencao/cadastrar_manutencao`: View para cadastrar novas manutenções.
- `home/veiculos/manutencao/editar_manutencao/<int:manutencao_id>`: View para editar uma manutenção existente.
- `home/veiculos/manutencao/deletar_manutencao/<int:manutencao_id>`: View para deletar uma manutenção existente.

### Checklists

- `home/veiculos/checklists`: View para listar os checklists.
- `home/veiculos/checklists/cadastrar_checklist`: View para cadastrar novos checklists.
- `home/veiculos/checklists/editar_checklist/<int:checklist_id>`: View para editar um checklist existente.
- `home/veiculos/checklist/deletar_checklist/<int:checklist_id>`: View para deletar um checklist existente.

### Motoristas

- `home/motoristas`: View para listar os motoristas.
- `home/motoristas/cadastrar_motorista`: View para cadastrar novos motoristas.
- `home/visualizar_documentos/<int:motorista_id>/`: View para visualizar os documentos de um motorista.
- `home/motoristas/editar_motorista/<int:motorista_id>`: View para editar um motorista existente.
- `home/motoristas/deletar_motorista/<int:motorista_id>`: View para deletar um motorista existente.

### Rotas

- `home/rotas`: View para listar as rotas.
- `home/rotas/cadastrar_rota`: View para cadastrar novas rotas.
- `home/rotas/editar_rota/<int:rota_id>`: View para editar uma rota existente.
- `home/rotas/deletar_rota/<int:rota_id>`: View para deletar uma rota existente.

### Combustível

- `home/combustivel`: View para listar os abastecimentos de combustível.
- `home/combustivel/cadastrar_abastecimento`: View para cadastrar novos abastecimentos de combustível.
- `home/view_comprovante_abastecimento/<int:abastecimento_id>/`: View para visualizar o comprovante de um abastecimento de combustível.
- `home/combustivel/editar_abastecimento/<int:abastecimento_id>`: View para editar um abastecimento de combustível existente.
- `home/combustivel/deletar_abastecimento/<int:abastecimento_id>`: View para deletar um abastecimento de combustível existente.

### Demandas de Transporte

- `home/demandas`: View para listar as demandas de transporte.
- `home/demandas/cadastrar_demanda`: View para cadastrar novas demandas de transporte.
- `home/demandas/editar_demanda/<int:demanda_id>`: View para editar uma demanda de transporte existente.
- `home/demandas/deletar/<int:demanda_id>`: View para deletar uma demanda de transporte existente.

### Viagens

- `home/viagens`: View para listar as viagens.
- `home/viagens/cadastrar_viagem`: View para cadastrar novas viagens.
- `home/viagens/editar_viagem/<int:viagem_id>`: View para editar uma viagem existente.
- `home/viagens/deletar_viagem/<int:viagem_id>`: View para deletar uma viagem existente.


