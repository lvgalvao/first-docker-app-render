# main.py
import os
import time
import threading
import boto3
from dotenv import load_dotenv
import streamlit as st

# Carregar variáveis de ambiente
load_dotenv()

# Configurações da AWS S3
bucket_name = os.getenv('AWS_BUCKET_NAME')
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)

# Lista global e Lock para sincronização
arquivos_encontrados = []
arquivos_lock = threading.Lock()

# Função para listar arquivos CSV
def listar_arquivos_csv():
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    arquivos_csv = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.csv')]
    return arquivos_csv

# Thread para monitorar novos arquivos
def monitorar_s3():
    global arquivos_encontrados
    while True:
        arquivos_csv_atual = listar_arquivos_csv()
        with arquivos_lock:  # Usar o Lock para sincronização
            novos_arquivos = [arq for arq in arquivos_csv_atual if arq not in arquivos_encontrados]
            for arquivo in novos_arquivos:
                print(f"Novo arquivo encontrado: {arquivo}")
                arquivos_encontrados.append(arquivo)
        time.sleep(30)

# Função principal do Streamlit
def streamlit_app():
    st.title('Lista de Arquivos CSV no S3')

    if st.button('Atualizar Lista'):
        with arquivos_lock:  # Sincronizar o acesso à lista global
            arquivos_atuais = listar_arquivos_csv()  # Sempre pegar a lista atual do bucket
        st.write(arquivos_atuais)

# Iniciar thread de monitoramento
threading.Thread(target=monitorar_s3, daemon=True).start()

# Executar aplicação Streamlit
if __name__ == '__main__':
    streamlit_app()
