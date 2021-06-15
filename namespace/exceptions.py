from fastapi import HTTPException, status


class NameSpaceExists(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs['detail'] = f'namespace with given name already exists'
        kwargs['status_code'] = status.HTTP_400_BAD_REQUEST
        super().__init__(*args, **kwargs)


class TokenNotValid(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs['detail'] = f'token is not valid'
        kwargs['status_code'] = status.HTTP_400_BAD_REQUEST
        super().__init__(*args, **kwargs)
