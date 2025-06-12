from fastapi.responses import JSONResponse

def ping():
    return JSONResponse({"status": "ok"})