import structlog
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pony.orm import db_session, select
from database import db
from datetime import datetime


def lambda_handler(event, context):
    logger = structlog.get_logger()
    logger.info(event)
    logger.info(context)

    failure_ids = []

    logger.info(f"Número de mensagens recebidas: {len(event.get('Records', []))}")

    result_data = event.get('Records', []).get('body')
    # Busca os dados da view no banco de dados
    headers = result_data.get('headers', [])
    rows = result_data.get('rows', [])

    # Autenticação com as credenciais do Google
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("cellular-block-362701-ea5b62201eea.json", scope)

    try:
        client = gspread.authorize(creds)
        # Tenta abrir a planilha pelo nome
        sheet = client.open("integration-planilha").sheet1
        logger.info("Conexão com a planilha Google Sheets bem-sucedida.")

        # Limpa a planilha e adiciona todas as novas linhas
        clear_and_add_rows(sheet, headers, rows)

    except Exception as e:
        logger.error(f"Could not process message with ID {result_data['messageId']}: {e}")
        failure_ids.append(result_data.get('messageId'))


def clear_and_add_rows(sheet, headers, rows):
    # Limpa todos os dados da planilha
    sheet.clear()

    # Adiciona os cabeçalhos
    sheet.append_row(headers)

    # Adiciona todas as linhas de dados
    if rows:
        sheet.append_rows(rows)