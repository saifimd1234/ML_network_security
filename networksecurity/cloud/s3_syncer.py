import os


class S3Sync:
    """
    A utility class to synchronize files between local directories and AWS S3 buckets.
    
    This class provides methods to upload (sync to S3) and download (sync from S3)
    files between a local directory and an S3 bucket using AWS CLI commands.
    
    Note:
        Requires AWS CLI to be installed and configured with appropriate credentials and permissions to access the specified S3 buckets.
    """
    
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        """
        Synchronize contents from a local folder to an AWS S3 bucket.
        
        This method runs the AWS CLI 's3 sync' command to upload the contents of
        the specified local folder to the specified S3 bucket URL, synchronizing
        only the files that have changed.
        
        Args:
            folder (str): Path to the local folder to be synchronized.
            aws_bucket_url (str): The AWS S3 bucket URL (e.g., 's3://bucket-name/prefix').
        
        Returns:
            None
        
        Example:
            >>> s3 = S3Sync()
            >>> s3.sync_folder_to_s3('./data', 's3://my-bucket/data')
        """
        command = f"aws s3 sync {folder} {aws_bucket_url} "
        os.system(command)

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        """
        Synchronize contents from an AWS S3 bucket to a local folder.
        
        This method runs the AWS CLI 's3 sync' command to download the contents of
        the specified S3 bucket URL to the specified local folder, synchronizing
        only the files that have changed.
        
        Args:
            folder (str): Path to the local folder where files will be downloaded.
            aws_bucket_url (str): The AWS S3 bucket URL (e.g., 's3://bucket-name/prefix').
        
        Returns:
            None
        
        Example:
            >>> s3 = S3Sync()
            >>> s3.sync_folder_from_s3('./data', 's3://my-bucket/data')
        """
        command = f"aws s3 sync  {aws_bucket_url} {folder} "
        os.system(command)

# We sync it with the cloud to have various version of the model and data.
# After installing AWS CLI, create a user in AWS IAM and configure the AWS CLI with the user's credentials.
# The user should have the necessary permissions to access the specified S3 bucket.
# Go to terminal here and write: aws configure
# Enter the access key, secret key, region(us-east-1), and output format(json) when prompted.
# Now the AWS CLI is configured with the user's credentials.
# Now we can use the S3Sync class to synchronize files between local directories and AWS S3 buckets.
# Run the app to check if everything is working fine, use: uvicorn app:app --reload