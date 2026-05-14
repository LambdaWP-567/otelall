from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

CONFIG_PATH = "/etc/otelcol-config/config.yaml"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    config_content = ""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            config_content = f.read()
    return templates.TemplateResponse(
        request=request, name="index.html", context={"config_content": config_content}
    )

@app.post("/save")
async def save_config(config: str = Form(...)):
    with open(CONFIG_PATH, "w") as f:
        f.write(config)
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
