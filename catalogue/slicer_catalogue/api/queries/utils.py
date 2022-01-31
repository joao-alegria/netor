import shutil
import urllib

import urllib.request
import json
from os import listdir
from pathlib import Path
from urllib.error import HTTPError

from mongoengine import DoesNotExist, MultipleObjectsReturned

from api.exceptions.exceptions import NotFoundException, MalformedTarFileException, IllegalStateException
from api.exceptions.utils import HTTPException, exception_message_elements
from http import HTTPStatus
from flask_mongoengine import current_mongoengine_instance

LOCAL_TEMP_DIR = "api/tmp"


def get_or_error(cls, status_code=HTTPStatus.NOT_FOUND, **kwargs):
    """
    @param cls: Model to be queried
    @param status_code: Http status code returned whenever a 'DoesNotExist' or 'MultipleObjectsReturned' exception is
    thrown
    @param kwargs: Query's arguments
    @return: Retrieve the the matching object raising an HttpException if multiple results or no results are found
    """

    try:
        return cls.objects.get(**kwargs)

    except DoesNotExist:
        class_name, args = exception_message_elements(cls, **kwargs)

        e = HTTPException(f"{class_name} with {args} not found in DB")
        e.code = status_code
        raise e

    except MultipleObjectsReturned:
        class_name, args = exception_message_elements(cls, **kwargs)

        e = HTTPException(f"Found multiple {class_name} objects with {args} in DB")
        e.code = status_code
        raise e


def transaction(callback):
    db = current_mongoengine_instance().connection
    with db.start_session() as session:
        session.with_transaction(callback)


def aggregate_transactions(transactions):
    def wrapper(session):
        for data in transactions:
            collection, operation, args = data.get('collection'), data.get('operation'), data.get('args')
            getattr(collection, operation)(*args, session=session)

    return wrapper


def download_file(remote_path, file_name):
    Path(LOCAL_TEMP_DIR).mkdir(parents=True, exist_ok=True)  # Create directory if not exists
    file_path = f'{LOCAL_TEMP_DIR}/{file_name}.tar'
    try:
        urllib.request.urlretrieve(remote_path, file_path)
    except HTTPError as e:
        raise NotFoundException(f'{e.msg}->{remote_path}')

    return file_path


def extract_file(path):
    extracted_folder_path = path.replace('.tar', '')
    try:
        shutil.unpack_archive(path, extracted_folder_path)
    except shutil.ReadError as e:
        raise MalformedTarFileException(e)

    return extracted_folder_path


def move_file(source_path, to_path=f"{LOCAL_TEMP_DIR}/cloud-config.txt"):
    shutil.move(source_path, to_path)


def remove_file_and_folder(file_path, folder_path):
    Path(file_path).unlink(missing_ok=False)
    shutil.rmtree(folder_path)


def file_exists(path):
    return Path(path).is_file()


def get_json_in_folder(folder_path):
    json_files = [f for f in listdir(folder_path) if f.endswith('.json')]

    if len(json_files) == 0:
        raise NotFoundException(f'Json file not found in {folder_path}')
    elif len(json_files) > 1:
        raise IllegalStateException(f'More than one json file found {folder_path}')

    try:
        with open(f'{folder_path}/{json_files[0]}') as json_file:
            content = json.load(json_file)
    except ValueError:
        raise IllegalStateException(f"Invalid json file extracted from vnf package path->{json_files[0]}")

    return content


def convert_all_fields_to_snake(data):
    if isinstance(data, list):
        return [convert_all_fields_to_snake(i) if isinstance(i, (dict, list)) else i for i in data]
    return {a.replace('-', '_'): convert_all_fields_to_snake(b) if isinstance(b, (dict, list)) else b for a, b in
            data.items()}
