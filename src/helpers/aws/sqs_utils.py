import json
import boto3
import structlog


def send_message_batch(object_list, object_id_key, queue_url, grouping_key=None):
    logger = structlog.get_logger()
    sqs = boto3.client('sqs')

    batch_list = [object_list[i:i + 10] for i in range(0, len(object_list), 10)]
    logger.info('{} pacote(s) preparados para envio.'.format(len(batch_list)))

    for i, batch in enumerate(batch_list, start=1):
        logger.info(f'Enviando pacote {i} para a fila.')
        sqs.send_message_batch(
            QueueUrl=queue_url,
            Entries=[{
                'Id': str(o[object_id_key]),
                'MessageBody': json.dumps(o),
                'MessageGroupId': str(o[grouping_key]) if grouping_key else '1'
            } for o in batch]
        )

    logger.info("Pacotes enviados com sucesso.")
