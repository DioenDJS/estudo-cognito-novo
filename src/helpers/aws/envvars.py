import os
import parameters, secrets

def get(key, default=None):
    result = os.getenv(key, default)
    result_str = str(result)

    if result is not None and result_str.startswith("parameters://"):
        tmp = result.split("://")[1]
        return parameters.get(tmp)

    if result is not None and result_str.startswith("secrets://"):
        tmp = result.split("://")[1].split("?")
        secret_name = tmp[0]
        secret_key = tmp[1] if len(tmp) > 1 else None
        return secrets.get(secret_name, secret_key)

    return result
