from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

import psutil, os
from urllib.parse import quote

app = FastAPI()


templates = Jinja2Templates(directory="templates")


@app.get("/{path:path}", response_class=HTMLResponse)
async def read_root(request: Request, path = ""):
    

    if not path:
        datas = [disk.device for disk in psutil.disk_partitions()]
    else:
        datas = os.listdir(path)
        datas = [{"path":quote(p),"name":p} for p in datas]
    return templates.TemplateResponse("index.html", 
                                    context={"request":request,
                                            "datas":datas})
