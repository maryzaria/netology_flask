from typing_extensions import Union


class HttpError(Exception):
    def __init__(self, status_code: int, description: Union[str, dict, list]):
        self.status_code = status_code
        self.description = description
