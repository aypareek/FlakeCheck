import yaml
import snowflake.connector


def load_config(path="config.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def get_snowflake_connection(config_path="config.yaml"):
    config = load_config(config_path)

    auth_method = config.get("auth_method", "externalbrowser")
    creds = config["snowflake"]

    conn_params = {
        "account": creds["account"],
        "user": creds["user"],
        "warehouse": creds["warehouse"],
        "database": creds["database"],
        "schema": creds["schema"],
    }

    if auth_method == "keypair":
        from snowflake.connector import pkey_pkcs8

        with open(config["keypair"]["private_key_path"], "rb") as key_file:
            private_key = pkey_pkcs8(
                key_file.read(),
                password=config["keypair"]["private_key_passphrase"].encode(),
            )
        conn_params["private_key"] = private_key
    else:
        conn_params["authenticator"] = "externalbrowser"

    conn = snowflake.connector.connect(**conn_params)
    return conn, config
