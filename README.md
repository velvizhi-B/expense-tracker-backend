## 💸 Expense Tracker

A full-featured **Expense Tracker** web API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. This project helps users manage their incomes, expenses, and bill reminders — and provides real-time financial summaries.

---

### 🚀 Features

* 🧑 User Registration and Login (JWT Auth)
* 💰 Track Incomes and Expense Records
* 🧾 Bill Reminders (with status)
* 📊 Financial Summary (total income, expenses, remaining balance)
* 🔐 Secure Protected Routes for User-specific data
* 🛆 Modular FastAPI Code Structure

---

### 💠 Technologies Used

* **Backend**: FastAPI (Python)
* **Database**: PostgreSQL
* **ORM**: SQLAlchemy
* **Security**: OAuth2, JWT
* **Others**: Pydantic, Uvicorn, Alembic (optional)

---

### 📁 Project Structure

```
app/
├── main.py                # Entry point
├── models/                # SQLAlchemy models
├── schemas/               # Pydantic schemas
├── routes/                # API routers (auth, expenses, incomes, etc.)
├── database/              # DB connection setup
├── auth_utils.py          # JWT and password handling
.env                       # Environment variables
requirements.txt           # Python dependencies
README.md
```

---

### ⚙️ Setup Instructions

#### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```

#### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set Up `.env` File

Create a `.env` file in the root:

```ini
DATABASE_URL=postgresql://username:password@localhost:5432/your_db_name
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### 5. Run the Server

```bash
uvicorn app.main:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the Swagger UI.

---

### 🔐 Authentication

* All protected routes require an **Authorization header**:

  ```
  Bearer <JWT_TOKEN>
  ```

---

### 📊 Summary API

Provides an overview of income, expenses, and remaining balance:

```
GET /summary
Headers: Authorization: Bearer <token>
```

---

### ✅ TODO / Improvements

* [ ] Add email verification
* [ ] Recurring bill automation
* [ ] Frontend UI (React/Next.js)
* [ ] Export reports (CSV/PDF)

---

### 🧑‍💻 Author

**Velvizhi B**
Final Year Student | Python & FastAPI Enthusiast

---

### 📝 License

This project is licensed under the **MIT License**.
