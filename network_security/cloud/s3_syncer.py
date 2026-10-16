import os
import subprocess
import logging


class S3Sync:
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        try:
            aws_executable = (
                r"C:\Program Files\Amazon\AWSCLIV2\aws.exe"
            )

            command = [
                aws_executable,
                "s3",
                "sync",
                folder,
                aws_bucket_url,
            ]

            subprocess.run(command, check=True)

            logging.info(
                f"Successfully synced {folder} to {aws_bucket_url}"
            )

        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to sync folder to S3: {e}")
            raise

        except FileNotFoundError as e:
            logging.error(f"AWS CLI executable not found: {e}")
            raise

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        try:
            aws_executable = (
                r"C:\Program Files\Amazon\AWSCLIV2\aws.exe"
            )

            command = [
                aws_executable,
                "s3",
                "sync",
                aws_bucket_url,
                folder,
            ]

            subprocess.run(command, check=True)

            logging.info(
                f"Successfully synced {aws_bucket_url} to {folder}"
            )

        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to sync folder from S3: {e}")
            raise

        except FileNotFoundError as e:
            logging.error(f"AWS CLI executable not found: {e}")
            raise

