from fastapi import HTTPException, status


class InvalidCredentialNames(HTTPException):
    def __init__(self, *args, **kwargs):
        invalid_credentials = kwargs.pop('invalid_credentials')
        valid_credentials = kwargs.pop('valid_credentials')

        kwargs['status_code'] = status.HTTP_400_BAD_REQUEST
        kwargs['detail'] = f'invalid credential names: {invalid_credentials}' \
                           f'.\nvalid ones are: {valid_credentials}'
        super().__init__(*args, **kwargs)


class ServiceInstanceExists(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs['detail'] = f'service instance already exists'
        kwargs['status_code'] = status.HTTP_400_BAD_REQUEST
        super().__init__(*args, **kwargs)
