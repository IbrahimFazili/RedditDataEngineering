from utils.constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import s3fs

def connect_to_s3():
    try:
        s3 = s3fs.S3FileSystem(
            anon=False,
            key=AWS_ACCESS_KEY_ID,
            secret=AWS_SECRET_ACCESS_KEY
        )
        return s3
    except Exception as e:
        print("Could not connect to S3. Error: ", e)


def create_s3_bucket_if_not_exists(s3, bucket_name):
    """
    Create an S3 bucket if it does not already exist.

    Args:
        s3 (s3fs.S3FileSystem): The S3 file system object.
        bucket_name (str): The name of the bucket to create.

    Returns:
        None

    Raises:
        Exception: If there is an error creating the S3 bucket.

    """
    try:
        if not s3.exists(bucket_name):
            s3.mkdir(bucket_name)
            print("Bucket created: ", bucket_name)
        else:
            print("Bucket already exists: ", bucket_name)
    except Exception as e:
        print("Could not create S3 bucket. Error: ", e)

def upload_to_s3(s3: s3fs.S3FileSystem, file_path: str, bucket:str, s3_file_name: str):
    try:
        s3.put(file_path, bucket + '/raw/' + s3_file_name)
        print('File uploaded to S3 bucket')
    except FileNotFoundError:   
        print("The file was not found")