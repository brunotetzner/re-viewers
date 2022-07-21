# fazendo o pull da imagem oficial no Docker Hub
FROM python:3.8

# setando variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copiando os requisitos necessários para a aplicação rodar
COPY ./requirements.txt .

# executando a instalação dos pacotes
RUN  pip install --upgrade pip && pip install -r requirements.txt 

# definindo o diretório de trabalho no contêiner
WORKDIR /code

# copiando todos os arquivos para o diretório de trabalho
COPY . /code/

# atualiza a lista de programas da máquina 
# e instalando a biblioteca bibpq-dev gccc
RUN apt update && apt install -y libpq-dev gcc

# instalando a biblioteca psycopg2
RUN pip install psycopg2