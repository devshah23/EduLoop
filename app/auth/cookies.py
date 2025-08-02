from fastapi.responses import JSONResponse

def create_cookie(response:JSONResponse,key:str,value:str,max_age:int):
    response.set_cookie(
        key=key,
        value=value,
        httponly=True,
        secure=False,
        max_age=max_age,
    )
    return response
