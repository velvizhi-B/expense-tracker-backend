from fastapi import FastAPI
from app import models, database
# import auth route here
from app.routes import auth, users, expenses, incomes, bill_reminders, summary
from fastapi.middleware.cors import CORSMiddleware
from app.routes import reports

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)     # include auth
app.include_router(users.router)    # include user routes (optional for now)
app.include_router(expenses.router)
app.include_router(incomes.router)
app.include_router(bill_reminders.router)
app.include_router(summary.router)
app.include_router(reports.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Expense Tracker API!"}
 # add expenses
  # add this
