import os
import sys
import argparse
import logging

import paramiko
import subprocess
sys.path.append("./")
from scripts.utils import (
    LoginAndGetToken,
    SecretManager,
    logging_configurator
)


REMOTE_PATH = "/encrypted"
SFTP_HOSTNAME = "inbox.ega-archive.org"
SFTP_PORT = 22


def get_active_account() -> str:
    """Helper function to determine which gcloud account is running the workflow"""
    try:
        result = subprocess.run(
            ['gcloud', 'auth', 'list', '--filter=status:ACTIVE', '--format=value(account)'],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
    except Exception as e:
        raise Exception(f"Exception: {str(e)}")


def transfer_file(encrypted_data_file: str, ega_inbox: str, password: str) -> None:
    """Transfer encrypted data file to EGA inbox via SFTP."""
    try:
        # Establish an SFTP connection
        with paramiko.Transport((SFTP_HOSTNAME, SFTP_PORT)) as transport:
            transport.connect(username=ega_inbox, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)

            # Upload the encrypted data file
            remote_file = os.path.join(REMOTE_PATH, os.path.basename(encrypted_data_file))
            sftp.put(encrypted_data_file, remote_file)

        logging.info(f"Successfully transferred {encrypted_data_file} to EGA inbox {ega_inbox}")
    except Exception as e:
        raise Exception(f"Error transferring file: {str(e)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Transfer a file to EGA using an FTP server"
    )
    parser.add_argument(
        "--encrypted_data_file",
        required=True,
        help="Data file that is already encrypted"
    )
    parser.add_argument(
        "--ega_inbox",
        required=True,
        help="Inbox assigned to the current PM"
    )
    args = parser.parse_args()

    # Retrieve the secret value from Google Secret Manager
    password = SecretManager(ega_inbox=args.ega_inbox).get_ega_password_secret()
    access_token = LoginAndGetToken(username=args.ega_inbox, password=password).login_and_get_token()

    logging.info("Starting script to transfer file to EGA")
    transfer_file(args.encrypted_data_file, args.ega_inbox, password)

    logging.info("Script finished")
