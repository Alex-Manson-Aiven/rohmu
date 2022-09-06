"""
rohmu

Copyright (c) 2016 Ohmu Ltd
Copyright (c) 2022 Aiven, Helsinki, Finland. https://aiven.io/
See LICENSE for details
"""
from .errors import InvalidConfigurationError
from .object_storage.base import BaseTransfer
from typing import Any, Dict, Mapping, Type

IO_BLOCK_SIZE = 2**20  # 1 MiB
STORAGE_TYPE = "storage_type"
Config = Mapping[str, Any]


def get_class_for_transfer(obj_store: Config) -> Type[BaseTransfer]:
    storage_type = obj_store[STORAGE_TYPE]
    if storage_type == "azure":
        from .object_storage.azure import AzureTransfer

        return AzureTransfer
    elif storage_type == "google":
        from .object_storage.google import GoogleTransfer

        return GoogleTransfer
    elif storage_type == "sftp":
        from .object_storage.sftp import SFTPTransfer

        return SFTPTransfer
    elif storage_type == "local":
        from .object_storage.local import LocalTransfer

        return LocalTransfer
    elif storage_type == "s3":
        from .object_storage.s3 import S3Transfer

        return S3Transfer
    elif storage_type == "swift":
        from .object_storage.swift import SwiftTransfer

        return SwiftTransfer

    raise InvalidConfigurationError("unsupported storage type {0!r}".format(storage_type))


def get_transfer(storage_config: Config) -> BaseTransfer:
    storage_class = get_class_for_transfer(storage_config)
    storage_config = dict(storage_config)
    storage_config.pop(STORAGE_TYPE)
    return storage_class(**storage_config)
