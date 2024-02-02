from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

import psutil, os
from urllib.parse import quote
import socket
import uvicorn


host = socket.gethostbyname(socket.gethostname())
app = FastAPI()



templates = Jinja2Templates(directory=os.path.dirname(__file__)+"/templates")

@app.get("/{path:path}", response_class=HTMLResponse)
async def read_root(request: Request, path = ""):
    

    if not path:
        datas = [disk.device for disk in psutil.disk_partitions()]
    else:
        file = request.url.path[:-1]
        if file.startswith("/"):
            file = file[1:]
        if not os.path.isdir(file):
            print(os.path.basename(file))
            return FileResponse(file, filename=os.path.basename(file))
            
            
        datas = os.listdir(path)
        datas = [{"path":quote(p),"name":p} for p in datas]
        
        
    return templates.TemplateResponse("index.html", 
                                    context={"request":request,
                                            "datas":datas})


if __name__=="__main__":
    uvicorn.run(app=app)