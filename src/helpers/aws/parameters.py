import boto3


def get_value(key) -> str:
    tmp = key.split("://")[1]
    return get(tmp)


def get(key) -> str:
    ssm = boto3.client("ssm")
    result = ssm.get_parameter(Name=key, WithDecryption=True)

    return result["Parameter"]["Value"]
