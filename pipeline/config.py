import os
from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}

config["BUCKET_NAME"] = config["BUCKET_NAME"] if 'BUCKET_NAME' in config else None
config["DB_CONNECTION"] = config["DB_CONNECTION"] if 'DB_CONNECTION' in config else None