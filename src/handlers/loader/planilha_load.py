import structlog
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import boto3
from botocore.exceptions import ClientError
import json


def lambda_handler(event, context):
    logger = structlog.get_logger()
    logger.info(event)
    logger.info(context)

    failure_ids = []

    logger.info(f"Número de mensagens recebidas: {len(event.get('Records', []))}")

    for record in event.get('Records', []):
        result_data = json.loads(record.get('body'))
        # Busca os dados da view no banco de dados
        headers = result_data.get('headers', [])
        rows = result_data.get('rows', [])

        # Nome do bucket S3 e chave do objeto
        bucket_name = "nome-do-seu-bucket"
        s3_key = "cellular-block-362701-ea5b62201eea.json"

        # Baixa o arquivo JSON do S3
        json_file_path = '/tmp/cellular-block-362701-ea5b62201eea.json'
        s3 = boto3.client('s3')

        try:
            s3.download_file(bucket_name, s3_key, json_file_path)
            logger.info("Arquivo JSON baixado do S3 com sucesso.")
        except ClientError as e:
            logger.error(f"Erro ao baixar o arquivo JSON do S3: {e}")
            failure_ids.append(record.get('messageId'))
            continue

        # Autenticação com as credenciais do Google
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
            client = gspread.authorize(creds)
            # Tenta abrir a planilha pelo nome
            sheet = client.open("integration-planilha").sheet1
            logger.info("Conexão com a planilha Google Sheets bem-sucedida.")

            # Limpa a planilha e adiciona todas as novas linhas
            clear_and_add_rows(sheet, headers, rows)

        except Exception as e:
            logger.error(f"Could not process message with ID {record.get('messageId')}: {e}")
            failure_ids.append(record.get('messageId'))


def clear_and_add_rows(sheet, headers, rows):
    # Limpa todos os dados da planilha
    sheet.clear()

    # Adiciona os cabeçalhos
    sheet.append_row(headers)

    # Adiciona todas as linhas de dados
    if rows:
        sheet.append_rows(rows)
