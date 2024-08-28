import requests
import logging
import re
import sys
import google_crc32c
from google.cloud import secretmanager
from typing import Optional

LOGIN_URL = "https://idp.ega-archive.org/realms/EGA/protocol/openid-connect/token"
SUBMISSION_PROTOCOL_API_URL = "https://submission.ega-archive.org/api"
VALID_STATUS_CODES = [200, 201]


class LoggingConfigurator:
    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        # Define a custom formatter
        formatter = logging.Formatter('%(levelname)s: %(asctime)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # Create a stderr handler
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.ERROR)
        stderr_handler.setFormatter(formatter)

        # Create a stdout handler
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)
        stdout_handler.setFormatter(formatter)

        # Get the root logger and add both handlers
        root_logger = logging.getLogger()
        root_logger.addHandler(stderr_handler)
        root_logger.addHandler(stdout_handler)

        # Set the level of the root logger to INFO
        root_logger.setLevel(logging.INFO)


# Instantiate LoggingConfigurator when this module is imported
logging_configurator = LoggingConfigurator()


class LoginAndGetToken:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def login_and_get_token(self) -> Optional[str]:
        """Logs in and retrieves access token"""
        response = requests.post(
            url=LOGIN_URL,
            data={
                "grant_type": "password",
                "client_id": "sp-api",
                "username": self.username,
                "password": self.password,
            }
        )
        if response.status_code in VALID_STATUS_CODES:
            token = response.json()["access_token"]
            print("Successfully created access token!")
            return token
        else:
            error_message = f"""Received status code {response.status_code} with error {response.json()} while 
            attempting to get access token"""
            print(error_message)
            raise Exception(error_message)


def format_request_header(token: str) -> dict:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }


def get_file_metadata_for_one_sample_in_inbox(
    normalized_sample_alias: str, headers: dict
) -> Optional[List[Dict]]:
    """
    Retrieves file metadata for file matching normalized sample alias in the inbox
    Endpoint documentation located here:
    https://submission.ega-archive.org/api/spec/#/paths/files/get
    """

    response = requests.get(
        url=f"{SUBMISSION_PROTOCOL_API_URL}/files?prefix=/{normalized_sample_alias}.cram",
        headers=headers,
    )
    if response.status_code in VALID_STATUS_CODES:
        file_metadata = response.json()

        if file_metadata:
            return file_metadata
        else:
            raise Exception("Expected to find at least 1 file in the inbox. Instead found none.")

    else:
        error_message = f"""Received status code {response.status_code} with error: {response.text} while
                 attempting to query for file metadata"""
        logging.error(error_message)
        raise Exception(error_message)


def normalize_sample_alias(sample_alias):
    """
    Normalizes sample alias by replacing any special characters with '_'
    """
    return re.sub(r"[!\"#$%&''()*/:;<=>?@\[\]\^`{|}~ ]", "_", sample_alias)


class SecretManager:
    def __init__(self, ega_inbox: str, project_id: str = "sc-ega-submissions", version_id: int = 1):
        self.project_id = project_id
        self.version_id = version_id
        self.ega_inbox = ega_inbox

    def _get_secret_version_name(self) -> str:
        secret_id = f"{self.ega_inbox}_password"
        return f"projects/{self.project_id}/secrets/{secret_id}/versions/{self.version_id}"

    @staticmethod
    def _validate_payload_checksum(response) -> int:
        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)

        return response.payload.data_crc32c == int(crc32c.hexdigest(), 16)

    def _access_secret_version(self):
        client = secretmanager.SecretManagerServiceClient()
        name = self._get_secret_version_name()
        
        try:
            response = client.access_secret_version(request={"name": name})
            if self._validate_payload_checksum(response):
                logging.info("Successfully accessed secret")

                return response.payload.data.decode("UTF-8")
            else:
                logging.error("Data corruption detected.")
        except Exception as e:
            raise Exception(f"Failed to access secret: {str(e)}")

        return None

    def get_ega_password_secret(self):
        secret_payload = self._access_secret_version()

        if secret_payload is None:
            raise ValueError("Unable to retrieve secret. Application will now exit.")

        return secret_payload
