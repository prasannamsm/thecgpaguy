from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.authoring.router import router as authoring_router
from app.runtime.router import router as runtime_router

app = FastAPI(title="TheCGPAGuy", version="0.1.0")

app.include_router(authoring_router, prefix="/authoring", tags=["Authoring"])
app.include_router(runtime_router, prefix="/runtime", tags=["Runtime"])

frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="frontend_assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("authoring/") or full_path.startswith("runtime/") or full_path == "":
            return FileResponse(str(frontend_dist / "index.html"))
        file = frontend_dist / full_path
        if file.exists() and file.is_file():
            return FileResponse(str(file))
        return FileResponse(str(frontend_dist / "index.html"))
else:
    @app.get("/")
    async def root():
        return {"app": "TheCGPAGuy", "status": "running", "frontend": "not built"}
