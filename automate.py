from fastapi import APIRouter, Query, HTTPException
import logging
from pathlib import Path
import os
import shutil
import json

router = APIRouter(prefix="/automate", tags=["Automate"])

# basic logging setup
logging.basicConfig(
    filename="organiser.log",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Config 
CONFIG_PATH = Path(__file__).parent / "file_types.json"

def load_file_types() -> dict:
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)
    

# Core Logic
def get_category(extension: str, file_types: dict) -> str:
    for category, extensions in file_types.items():
        if extension.lower() in extensions:
            return category
    return "Others"

def organise_folder(folder_path: str):
    path = Path(folder_path)
    
    if not path.exists():
        raise HTTPException(status_code=400, detail=f"Path does not exist: {folder_path}")
    if not path.is_dir():
        raise HTTPException(status_code=400, detail=f"Path is not a folder: {folder_path}")
    
    file_types = load_file_types()
    
    moved = []     
    skipped = []    
    errors = []     

    logger.info("=" * 50)
    logger.info("Organising folder: %s", folder_path)
    
    for file in path.iterdir():
        if not file.is_file():
            logger.debug("Skipped (not a file): %s", file.name)
            skipped.append(file.name)
            continue

        extension = file.suffix         
        category  = get_category(extension, file_types)

        dest_folder = path / category
        dest_folder.mkdir(exist_ok=True)

        dest_path = dest_folder / file.name

        if dest_path.exists():
            dest_path = dest_folder / f"{file.stem}_duplicate{file.suffix}"

        try:
            shutil.move(str(file), str(dest_path))
            logger.info("Moved: %s  →  %s/", file.name, category)
            moved.append({"file": file.name, "moved_to": category})
        except Exception as e:
            logger.error("Failed to move %s: %s", file.name, str(e))
            errors.append({"file": file.name, "error": str(e)})

    logger.info("Done — moved: %d, skipped: %d, errors: %d", len(moved), len(skipped), len(errors))

    return {
        "folder": folder_path,
        "moved": moved,
        "skipped": skipped,
        "errors": errors,
        "summary": {
            "total_moved": len(moved),
            "total_skipped": len(skipped),
            "total_errors": len(errors),
        }
    }
    
    
@router.get("/run")
def run_script(folder_path: str = Query(..., description="Full path to the folder you want to organise")):
    logger.info("Received /run request — folder_path: %s", folder_path)
    result = organise_folder(folder_path)
    return result