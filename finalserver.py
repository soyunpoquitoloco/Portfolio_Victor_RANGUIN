from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

# Middleware pour autoriser les requêtes CORS
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],  # Autoriser toutes les origines (pour le développement)
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

# Modèle de données pour un projet
class Project(BaseModel):
   image_url: str
   description: str

# Stockage en mémoire pour les projets
projects = []

@app.post("/projects/")
async def add_project(project: Project):
   projects.append(project)
   return project

@app.get("/projects/")
async def get_projects():
   return projects

@app.delete("/projects/{project_index}")
async def delete_project(project_index: int):
   if project_index < 0 or project_index >= len(projects):
       raise HTTPException(status_code=404, detail="Project not found")
   deleted_project = projects.pop(project_index)
   return deleted_project

@app.get("/", response_class=HTMLResponse)
async def read_root():
   with open("Final.html", "r") as f:
       return f.read()

@app.put("/projects/{project_index}")
async def update_project(project_index: int, updated_project: Project):
   if project_index < 0 or project_index >= len(projects):
       raise HTTPException(status_code=404, detail="Project not found")
   projects[project_index] = updated_project
   return updated_project
