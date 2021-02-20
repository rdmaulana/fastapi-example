from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
import models, schemas

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def update(id : int, request: schemas.Blog, db: Session):
    dt = db.query(models.Blog).filter(models.Blog.id == id)
    if not dt.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Blog with id {id} not found"
        )
    
    dt.update(request)
    db.commit()
    return 'Success update data.' 

def show(id : int, response: Response, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog

def delete(id : int ,db: Session):
    dt = db.query(models.Blog).filter(models.Blog.id == id)
    if not dt.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Blog with id {id} not found"
        )
    
    dt.delete(synchronize_session=False)
    db.commit()
    return f"Blog {id} has been deleted."