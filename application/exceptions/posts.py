from fastapi import HTTPException, status


class PostNotFoundError(HTTPException):
    def __init__(self, detail: str = "Post not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
