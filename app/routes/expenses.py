from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth_utils import get_current_user
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/expenses", tags=["Expenses"])


# ▶️ CREATE Expense
@router.post("/", response_model=schemas.ExpenseResponse)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_expense = models.Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        expense_date=expense.expense_date,
        user_id=current_user.id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


# 📥 READ All Expenses of Current User
@router.get("/", response_model=list[schemas.ExpenseResponse])
def get_expenses(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    expenses = db.query(models.Expense).filter(models.Expense.user_id == current_user.id).all()
    return expenses


# 🔍 READ Single Expense by ID
@router.get("/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


# ✏️ UPDATE Expense
@router.put("/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(
    expense_id: int,
    updated_data: schemas.ExpenseCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.title = updated_data.title
    expense.amount = updated_data.amount
    expense.category = updated_data.category
    expense.expense_date = updated_data.expense_date

    db.commit()
    db.refresh(expense)
    return expense


# ❌ DELETE Expense


@router.delete("/{expense_id}", response_model=schemas.ExpenseResponse)
def delete_expense(
    expense_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Fetch the expense belonging to the current user
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    # Copy the data to return before deleting
    deleted_expense = expense

    db.delete(expense)
    db.commit()
    
    return deleted_expense


