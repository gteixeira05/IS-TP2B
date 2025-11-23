TP2-B — XML-RPC, gRPC & Docker
==============================================

Este projeto demonstra a comunicação interprocesso utilizando os protocolos XML-RPC e gRPC, com contentorização via Docker.

----------------------------------------------
ESTRUTURA DO PROJETO
----------------------------------------------
* grpc_server.py, grpc_client.py   — Servidor e cliente gRPC
* xml_rpc_server.py, xml_rpc_client.py — Servidor e cliente XML-RPC
* sales.proto, sales_pb2.py, sales_pb2_grpc.py — Ficheiros Protobuf/gRPC
* csv_to_xml.py, xml_validator.py, xpath_query.py — Utilitários de processamento e validação
* Retail-Supply-Chain-Sales-Dataset.* — Datasets (XML, CSV, XLSX, XSD)
* Dockerfile.grpc, Dockerfile.xmlrpc — Dockerfiles para cada servidor
* README.txt — Este ficheiro (na raiz do projeto, junto aos scripts e Dockerfiles)

----------------------------------------------
REQUISITOS
----------------------------------------------
* Python 3.11+
* pip (para gestão de pacotes Python)
* Docker Desktop/CLI (para contentorização)

----------------------------------------------
COMO CORRER LOCALMENTE (SEM DOCKER)
----------------------------------------------

1. Clonar repositório:
git clone https://github.com/gteixeira05/IS-TP2B.git
cd IS-TP2B

2. Instalar dependências:
python -m venv venv311
source venv311/bin/activate
pip install grpcio grpcio-tools protobuf lxml

3. Executar Servidor e Cliente XML-RPC:
# Terminal 1 (Servidor)
python xml_rpc_server.py
# Terminal 2 (Cliente)
python xml_rpc_client.py

4. Executar Servidor e Cliente gRPC:
# Terminal 1 (Servidor)
python grpc_server.py
# Terminal 2 (Cliente)
python grpc_client.py

----------------------------------------------
COMO CORRER COM DOCKER
----------------------------------------------

1. Servidor gRPC:
# Construir a imagem
docker build -f Dockerfile.grpc -t tp2b-grpc .
# Correr o container (-p 50051:50051)
docker run -p 50051:50051 tp2b-grpc

2. Servidor XML-RPC:
# Construir a imagem
docker build -f Dockerfile.xmlrpc -t tp2b-xmlrpc .
# Correr o container (-p 8000:8000)
docker run -p 8000:8000 tp2b-xmlrpc
# NOTA: O server XML-RPC usa ("0.0.0.0", 8000) no Docker para aceitar ligações externas.

3. Executar Clientes (com o servidor a correr no Docker):
# Cliente gRPC
python grpc_client.py
# Cliente XML-RPC
python xml_rpc_client.py

----------------------------------------------
NOTAS GERAIS
----------------------------------------------
* O ficheiro .gitignore ignora o ambiente virtual (venv) e ficheiros temporários.
* Sempre que alterar o código do servidor (grpc_server.py ou xml_rpc_server.py), faça rebuild do container Docker correspondente.
* Os prints de output dos servidores e clientes (ex: "DEBUG: Servidor XML-RPC arrancou!", "Vendas no Top 10 por categoria...") são importantes para a validação/teste.