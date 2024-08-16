import structlog
from helpers.aws import sqs_utils
from datetime import datetime, timezone


def lambda_handler(event, context):
    # queue_url = envvars.get("SHEETS_QUEUE_URL")
    try:
        logger = structlog.get_logger()
        logger.info('Iniciando extração de registros.')
        logger.info(event)
        logger.info(context)

        result ={
            "description": ['data_lancamento', 'projeto', 'descricao', 'valor', 'valor_absoluto', 'origem', 'cliente', 'status', 'categoria'],
            "rows": [(datetime(2021, 9, 1, 0, 0, tzinfo=timezone.utc), 'Projeto_x - Alocações', 'Colçaborador_um', -63.2405846, 61.2735846, 'Folha de pagamento', 'projeto', 'PAGO', 'CUSTO PROFISSIONAIS CLT'),
                     (datetime(2022, 9, 1, 0, 0, tzinfo=timezone.utc), 'Projeto_y - Alocações', 'Colçaborador_um', -12.54774, 12.5471074, 'Folha de pagamento', 'projeto', 'PAGO', 'SALARIOS E ORDENADOS'),
                     (datetime(2024, 9, 1, 0, 0, tzinfo=timezone.utc), 'Projeto_b - Alocação B', 'Colçaborador_dois', -75.7879245, 76.7879245, 'Folha de pagamento', 'projeto', 'PAGO', 'VALE ALIMENTAÇAO')]
        }

        # Extrai os cabeçalhos das colunas da view
        headers = result["description"]

        rows = result["rows"]

        # Converte objetos datetime em strings
        converted_rows = []
        converted_row = []
        for row in rows:

            for value in row:
                if isinstance(value, datetime):
                    converted_row.append(value.strftime('%Y-%m-%d %H:%M:%S'))  # Formato de data desejado
                else:
                    converted_row.append(value)

        converted_rows.append({"headers":headers, "rows": converted_row, "codigo":1})

        sqs_utils.send_message_batch(object_list=converted_rows, object_id_key='codigo', queue_url=queue_url)
    except Exception as e:
        logger.error(f'Erro encontrado durante a integração: {str(e)}')
        raise e

