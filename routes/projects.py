from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Project, ProjectCreate
from database import get_session
from dependencies import get_current_user, admin_required

router = APIRouter()

@router.get("/projects", response_model=list[Project])
def get_projects(session: Session = Depends(get_session), user=Depends(get_current_user)):
    return session.exec(select(Project)).all()

@router.post("/projects", response_model=Project)
def create_project(project: ProjectCreate, session: Session = Depends(get_session), admin=Depends(admin_required)):
    new_project = Project(name=project.name, description=project.description)
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
    return new_project

@router.delete("/projects/{project_id}")
def delete_project(project_id: int, session: Session = Depends(get_session), admin=Depends(admin_required)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"message": "Project deleted"}

@router.put("/projects/{project_id}", response_model=Project)
def update_project(project_id: int, updated: ProjectCreate, session: Session = Depends(get_session), admin=Depends(admin_required)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.name = updated.name
    project.description = updated.description
    session.add(project)
    session.commit()
    session.refresh(project)
    return project
