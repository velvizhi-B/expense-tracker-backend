# app/routes/summary.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, database, schemas
from app.auth_utils import get_current_user

router = APIRouter(prefix="/summary", tags=["Summary"])

@router.get("/", response_model=schemas.SummaryResponse)
def get_summary(db: Session = Depends(database.get_db),
                current_user: models.User = Depends(get_current_user)):

    # Total Income
    total_income = db.query(func.coalesce(func.sum(models.Income.amount), 0)) \
                     .filter(models.Income.user_id == current_user.id).scalar()

    # Total Expenses
    total_expenses = db.query(func.coalesce(func.sum(models.Expense.amount), 0)) \
                       .filter(models.Expense.user_id == current_user.id).scalar()

    # Remaining Balance
    remaining_balance = total_income - total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "remaining_balance": remaining_balance
    }
