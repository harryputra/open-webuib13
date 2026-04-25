import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
WORKSPACE_DIR = "/file_rag"

class WriteRequest(BaseModel):
    content: str

@router.get("/list")
async def list_files(path: str = ""):
    full_path = os.path.abspath(os.path.join(WORKSPACE_DIR, path))
    if not full_path.startswith(WORKSPACE_DIR):
         raise HTTPException(status_code=403, detail="Forbidden path")
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="Path not found")
    items = []
    for entry in os.scandir(full_path):
        items.append({
            "name": entry.name,
            "path": os.path.relpath(entry.path, WORKSPACE_DIR).replace("\\", "/"),
            "is_dir": entry.is_dir()
        })
    return items

@router.get("/read")
async def read_file(path: str):
    full_path = os.path.abspath(os.path.join(WORKSPACE_DIR, path))
    if not full_path.startswith(WORKSPACE_DIR) or not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(full_path, 'r', encoding='utf-8') as f:
        return {"content": f.read()}

@router.post("/write")
async def write_file(path: str, request: WriteRequest):
    full_path = os.path.abspath(os.path.join(WORKSPACE_DIR, path))
    if not full_path.startswith(WORKSPACE_DIR):
         raise HTTPException(status_code=403, detail="Forbidden")
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(request.content)
    return {"status": "success"}
