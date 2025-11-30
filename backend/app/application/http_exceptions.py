from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)
