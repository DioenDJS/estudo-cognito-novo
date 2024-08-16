import structlog


def lambda_handler(event, context):
    logger = structlog.get_logger()
    logger.info(event)
    logger.info(context)

    failure_ids = []

    logger.info(f"Número de mensagens recebidas: {len(event.get('Records', []))}")

    for message in event.get('Records', []):
        try:
            logger.info(message)


        except Exception as e:
            logger.error(f"Could not process message with ID {message['messageId']}: {e}")
            failure_ids.append(message.get('messageId'))
