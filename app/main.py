from fastapi import FastAPI
from app import models, database
from app.routes import auth, users, expenses, incomes, bill_reminders, summary    # import auth route here

app = FastAPI()

# Optional: only if you want to create tables from SQLAlchemy
# models.Base.metadata.create_all(bind=database.engine)

app.include_router(auth.router)     # include auth
app.include_router(users.router)    # include user routes (optional for now)
app.include_router(expenses.router) 
app.include_router(incomes.router)
app.include_router(bill_reminders.router)
app.include_router(summary.router)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Expense Tracker API!"}
 # add expenses
  # add this
