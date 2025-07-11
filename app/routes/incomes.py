from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth_utils import get_current_user

router = APIRouter(prefix="/incomes", tags=["Incomes"])

# Create income
@router.post("/", response_model=schemas.IncomeResponse)
def create_income(income: schemas.IncomeCreate,
                  db: Session = Depends(database.get_db),
                  current_user: models.User = Depends(get_current_user)):
    new_income = models.Income(
        amount=income.amount,
        source=income.source,
        received_date=income.received_date,
        user_id=current_user.id
    )
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income


# Get all incomes of the current user
@router.get("/", response_model=list[schemas.IncomeResponse])
def get_incomes(db: Session = Depends(database.get_db),
                current_user: models.User = Depends(get_current_user)):
    incomes = db.query(models.Income).filter(models.Income.user_id == current_user.id).all()
    return incomes


# Get income by ID
@router.get("/{income_id}", response_model=schemas.IncomeResponse)
def get_income(income_id: int,
               db: Session = Depends(database.get_db),
               current_user: models.User = Depends(get_current_user)):
    income = db.query(models.Income).filter(
        models.Income.id == income_id,
        models.Income.user_id == current_user.id
    ).first()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")
    return income


# Update income
@router.put("/{income_id}", response_model=schemas.IncomeResponse)
def update_income(income_id: int, updated: schemas.IncomeCreate,
                  db: Session = Depends(database.get_db),
                  current_user: models.User = Depends(get_current_user)):
    income = db.query(models.Income).filter(
        models.Income.id == income_id,
        models.Income.user_id == current_user.id
    ).first()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")

    income.amount = updated.amount
    income.source = updated.source
    income.received_date = updated.received_date

    db.commit()
    db.refresh(income)
    return income


# Delete income
@router.delete("/{income_id}", response_model=schemas.IncomeResponse)
def delete_income(income_id: int,
                  db: Session = Depends(database.get_db),
                  current_user: models.User = Depends(get_current_user)):
    income = db.query(models.Income).filter(
        models.Income.id == income_id,
        models.Income.user_id == current_user.id
    ).first()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")

    deleted_income = income
    db.delete(income)
    db.commit()
    return deleted_income
