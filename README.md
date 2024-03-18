<h1 align="center"> ST-CAFS </h1>
<h2>Detalhes da Arquitetura e Integrações</h2>
<ul>
    <li>Implantação em <a href="https://www.python.org/">Python 3</a>;</li>
    <li>Foi feito uso do Framework <a href="https://www.djangoproject.com/">Django 4.2.8</a>;</li>
    <li>O banco de dados utilizado foi o <a href="https://www.postgresql.org/">PostgreSQL</a>, acesse o <a href="https://drive.google.com/file/d/1XSpE-rLkoXuwUgNRMDcwU5YNg_XaNQrS/view">diagrama de entidades e relacionamento(DER)</a> para uma visualização do modelo.</li>
    <li>As bibliotecas utilizadas pelo projeto estão presentes no arquivo requirements.txt na raiz do projeto.</li>
</ul>

<h2>Execução do Código</h2>
<p>Para a execução do código é necessário realizar algumas configurações:</p>
<ol>
    <li><strong>Configuração do Banco de Dados:</strong>
        <ul>
            <li>Configure o banco de dados no arquivo settings.py na raiz do projeto.
                <code>DATABASES</code>.</li>
        </ul>
    </li>
    <li><strong>Docker-Compose:</strong>
        <ul>
            <li>O projeto está configurado para execução com o <a href="https://docs.docker.com/compose/">docker-compose</a>, onde algumas variáveis de
                ambiente e dependências já estão configuradas.</li>
        </ul>
    </li>
    <li><strong>Rodar Migrações:</strong>
        <ul>
            <li>Execute as migrações do Django com os seguintes comandos:
                <br>
                <code>docker-compose run web python manage.py makemigrations</code>
                <br>
                <code>docker-compose run web python manage.py migrate</code>
            </li>
        </ul>
    </li>
    <li><strong>Rodar o Projeto:</strong>
        <ul>
            <li>Inicie o projeto com o seguinte comando:
                <br>
                <code>docker-compose up</code>
            </li>
        </ul>
    </li>
    <li><strong>Backup do banco de dados:</strong>
        <ul>
            <li>Configure o crontab para executar o script de backup todos os dias às 3h00, caso queira realizar um backup manual navegue até a pasta do projeto e utilize o seguinte comando:
                <br>
                <code>./backup.sh</code>
            </li>
            <li>Para realizar a restauração do banco de dados utilize o seguinte comando:
                <br>
                <code>docker exec -i db psql -U setorT setorT < /caminho/para/o/arquivo/de/backup.sql</code>
            </li>
        </ul>
    </li>
</ol>
<h2>Documentação</h2>
<p>Para ver a documentação navegue até a pasta docs na raiz do projeto e execute o seguinte comando:</p>
<code>mkdocs serve</code>
