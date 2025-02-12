import sys
import argparse
import logging
from pathlib import Path
from csv import DictWriter
from typing import Dict, List

sys.path.append("./")
from scripts.utils import (
    LoginAndGetToken,
    SecretManager,
    format_request_header,
    normalize_sample_alias,
    get_file_metadata_for_one_sample_in_inbox,
    logging_configurator,
)


class GetValidationStatus:
    VALID_STATUS_CODES = [200, 201]

    def __init__(self, token: str, sample_alias: str) -> None:
        self.token = token
        self.sample_alias = sample_alias

    def _headers(self):
        return format_request_header(self.token)

    def _get_file_info_for_sample(self, file_metadata) -> List[Dict]:
        logging.info(f"Attempting to find all files associated with sample alias {self.sample_alias}")
        files_for_sample = []
        normalized_alias = normalize_sample_alias(self.sample_alias)

        for file in file_metadata:
            relative_file_path = file["relative_path"]
            file_name = Path(relative_file_path).name
            sample_alias_from_path = Path(file_name).stem
            if sample_alias_from_path == normalized_alias:
                files_for_sample.append(file)

        if not files_for_sample:
            raise Exception(
                f"Expected to find at least 1 file associated with sample {self.sample_alias}, instead found none"
            )
        return files_for_sample

    def _determine_validation_status_for_files(self, files_metadata_for_sample: List[Dict]) -> bool:
        logging.info("Attempting to determine file validation status now.")
        validation_statuses = []
        for file in files_metadata_for_sample:
            # if the file has an encrypted checksum, and un-encrypted checksum, and the file size is larger than 0,
            # this indicates that the file is "valid"
            # TODO is file["status"] useful at all here?
            if file["encrypted_checksum"] and file["unencrypted_checksum"] and file["filesize"] > 0:
                validation_statuses.append(True)

        if all(validation_statuses):
            logging.info(f"File(s) associated with {self.sample_alias} are valid!")
            return True
        logging.info(f"File(s) associated wtih {self.sample_alias} have not yet been validated.")
        return False

    def get_file_validation_status(self) -> bool:
        # Get the metadata for ALL files in the submission
        logging.info("Attempting to collect metadata for sample in submission")
        normalized_alias = normalize_sample_alias(self.sample_alias)
        file_metadata = get_file_metadata_for_one_sample_in_inbox(
            normalized_alias, self._headers()
        )
        # Filter down to only the file metadata for the sample of interest
        if file_metadata:
            files_metadata_for_sample = self._get_file_info_for_sample(file_metadata=file_metadata)

            # If we find file(s) associated with the sample, find the OVERALL validation status
            if files_metadata_for_sample:
                all_files_valid = self._determine_validation_status_for_files(files_metadata_for_sample)
                return all_files_valid


class WriteOutputTsvFiles:
    def __init__(self, sample_alias: str, sample_id: str, validation_status: bool) -> None:
        self.sample_alias = sample_alias
        self.sample_id = sample_id
        self.validation_status = validation_status
        self.file_content = "validated" if self.validation_status else "incomplete"

    def _write_file_validation_status_file(self) -> None:
        logging.info("Writing final validation status out to file")
        with open("/cromwell_root/file_validation_status.tsv", "w") as validation_file:
            validation_file.write(self.file_content)

    def _write_validation_status_for_terra_data_tables(self) -> None:
        logging.info("Writing validation status and sample id tsv to file")
        with open("/cromwell_root/sample_id_validation_status.tsv", "w") as validation_file:
            writer = DictWriter(validation_file, fieldnames=["entity:sample_id", "file_validation_status"], delimiter='\t')
            writer.writeheader()
            writer.writerow({"entity:sample_id": self.sample_id, "file_validation_status": self.file_content})

    def write_output_files(self):
        self._write_file_validation_status_file()
        self._write_validation_status_for_terra_data_tables()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="This script will check the validation status of a file associated with the provided sample. "
                    "It will output two tsv files, one with the validation status and one tsv that can be used to load"
                    " the metadata into the Terra tables"
    )
    parser.add_argument(
        "-user_name",
        required=True,
        help="The EGA username"
    )
    parser.add_argument(
        "-sample_alias",
        required=True,
        type=str,
        help="The sample alias to register metadata for",
    )
    parser.add_argument(
        "-sample_id",
        required=True,
        help="The sample_id identifier from the terra data table"
    )
    args = parser.parse_args()

    password = SecretManager(ega_inbox=args.user_name).get_ega_password_secret()
    access_token = LoginAndGetToken(username=args.user_name, password=password).login_and_get_token()

    if access_token:
        logging.info("Successfully generated access token")
        validation_status = GetValidationStatus(
            token=access_token,
            sample_alias=args.sample_alias
        ).get_file_validation_status()

        WriteOutputTsvFiles(
            sample_alias=args.sample_alias,
            sample_id=args.sample_id,
            validation_status=validation_status
        ).write_output_files()
