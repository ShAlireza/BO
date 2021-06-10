from fastapi import HTTPException, status


class ServiceInstanceNotFound(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs['status_code'] = status.HTTP_400_BAD_REQUEST
        kwargs['detail'] = f'service instance not found in added instances'
        super().__init__(**kwargs)

