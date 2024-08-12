import structlog
import json


def lambda_handler(event, context):
    try:
        logger = structlog.get_logger()
        logger.info('Iniciando extração de registros.')
        logger.info(event)
        logger.info(context)

        return {
            'statusCode': 200,
            'headers': {
                "Content-Type": "application/json",  # Corrected typo
            },
            'body': json.dumps({
                "name": "Dioane",
                "email": "diovane2gmail.com"
            })

        }
    except Exception as e:
        logger.error(f'Erro encontrado durante a integração: {str(e)}')
        raise e
