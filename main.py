import boto3
import pandas as pd
import time
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações
bucket_name = os.getenv('AWS_BUCKET_NAME')
access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_DEFAULT_REGION')

# Configurar cliente S3 com credenciais explícitas (se necessário)
s3_client = boto3.client(
    's3',
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    region_name=region_name
)

def listar_arquivos_csv():
    """Lista todos os arquivos CSV no bucket especificado."""
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    arquivos_csv = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.csv')]
    return arquivos_csv

def carregar_csv_para_dataframe(nome_arquivo):
    """Carrega um arquivo CSV do S3 para um DataFrame do pandas."""
    obj = s3_client.get_object(Bucket=bucket_name, Key=nome_arquivo)
    df = pd.read_csv(obj['Body'])
    return df

def main():
    arquivos_processados = set()

    while True:
        print("Verificando por novos arquivos CSV...")
        arquivos_csv = listar_arquivos_csv()
        
        for arquivo in arquivos_csv:
            if arquivo not in arquivos_processados:
                print(f"Processando {arquivo}...")
                df = carregar_csv_para_dataframe(arquivo)
                print(df.head())  # Exemplo de manipulação: mostrar as primeiras linhas
                arquivos_processados.add(arquivo)
        
        time.sleep(30)  # Espera por 30 segundos antes de verificar novamente

if __name__ == '__main__':
    main()
