from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas, models
from app.api.dependencies import get_database

router = APIRouter(prefix="/projects", tags=["projects"])


def _convert_tags_to_list(project: models.Project) -> models.Project:
    if project.tags:
        project.tags = project.tags.split(",") if isinstance(project.tags, str) else project.tags
    return project


@router.get("/", response_model=List[schemas.ProjectResponse])
def get_projects(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_database)
):
    query = db.query(models.Project)
    
    if category:
        query = query.filter(models.Project.category == category)
    
    if featured is not None:
        query = query.filter(models.Project.is_featured == featured)
    
    projects = query.order_by(models.Project.created_at.desc()).offset(skip).limit(limit).all()
    for project in projects:
        _convert_tags_to_list(project)
    return projects


@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_database)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    _convert_tags_to_list(project)
    return project


@router.post("/", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_database)):
    db_project = models.Project(
        title=project.title,
        description=project.description,
        long_description=project.long_description,
        category=project.category,
        year=project.year,
        tags=",".join(project.tags) if project.tags else None,
        image_url=project.image_url,
        link=project.link,
        github=project.github,
        is_featured=project.is_featured
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    _convert_tags_to_list(db_project)
    return db_project


@router.put("/{project_id}", response_model=schemas.ProjectResponse)
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    db: Session = Depends(get_database)
):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    update_data = project_update.model_dump(exclude_unset=True)
    
    if "tags" in update_data and update_data["tags"] is not None:
        update_data["tags"] = ",".join(update_data["tags"])
    
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    
    _convert_tags_to_list(db_project)
    return db_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_database)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(db_project)
    db.commit()
    return None

