from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime
from io import BytesIO
import pandas as pd
from xhtml2pdf import pisa
from app import database, models
from app.auth_utils import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])


def generate_excel(incomes, expenses):
    income_df = pd.DataFrame([{
        "Type": "Income",
        "Amount": i.amount,
        "Source/Title": i.source,
        "Date": i.received_date
    } for i in incomes])

    expense_df = pd.DataFrame([{
        "Type": "Expense",
        "Amount": e.amount,
        "Source/Title": e.title,
        "Date": e.expense_date
    } for e in expenses])

    df = pd.concat([income_df, expense_df])
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output


def generate_pdf(incomes, expenses):
    html = "<h2>Expense Tracker Report</h2><table border='1'><tr><th>Type</th><th>Amount</th><th>Source/Title</th><th>Date</th></tr>"
    for i in incomes:
        html += f"<tr><td>Income</td><td>{i.amount}</td><td>{i.source}</td><td>{i.received_date}</td></tr>"
    for e in expenses:
        html += f"<tr><td>Expense</td><td>{e.amount}</td><td>{e.title}</td><td>{e.expense_date}</td></tr>"
    html += "</table>"

    pdf_file = BytesIO()
    pisa.CreatePDF(html, dest=pdf_file)
    pdf_file.seek(0)
    return pdf_file


@router.get("/full")
def download_full_report(
    format: str = Query(..., regex="^(excel|pdf)$"),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    incomes = db.query(models.Income).filter(models.Income.user_id == current_user.id).all()
    expenses = db.query(models.Expense).filter(models.Expense.user_id == current_user.id).all()

    if format == "excel":
        file = generate_excel(incomes, expenses)
        return StreamingResponse(file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 headers={"Content-Disposition": "attachment; filename=report.xlsx"})

    elif format == "pdf":
        file = generate_pdf(incomes, expenses)
        return StreamingResponse(file, media_type="application/pdf",
                                 headers={"Content-Disposition": "attachment; filename=report.pdf"})


@router.get("/range")
def download_range_report(
    from_date: str,
    to_date: str,
    format: str = Query(..., regex="^(excel|pdf)$"),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        start = datetime.strptime(from_date, "%Y-%m-%d").date()
        end = datetime.strptime(to_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    incomes = db.query(models.Income).filter(
        models.Income.user_id == current_user.id,
        models.Income.received_date.between(start, end)
    ).all()

    expenses = db.query(models.Expense).filter(
        models.Expense.user_id == current_user.id,
        models.Expense.expense_date.between(start, end)
    ).all()

    if format == "excel":
        file = generate_excel(incomes, expenses)
        return StreamingResponse(file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 headers={"Content-Disposition": "attachment; filename=datewise_report.xlsx"})

    elif format == "pdf":
        file = generate_pdf(incomes, expenses)
        return StreamingResponse(file, media_type="application/pdf",
                                 headers={"Content-Disposition": "attachment; filename=datewise_report.pdf"})
