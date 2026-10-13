from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from pathlib import Path
from functools import wraps
from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

BASE = Path(__file__).resolve().parent
DB = BASE / "library.db"

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin','librarian','student','faculty'))
    );

    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        category TEXT,
        isbn TEXT,
        shelf TEXT,
        status TEXT NOT NULL DEFAULT 'Available'
    );

    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        issue_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        return_date TEXT,
        fine REAL DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(book_id) REFERENCES books(id)
    );
    """)
    users = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]
    if users == 0:
        seed_users = [
            ("Administrator", "admin@library.com", "admin123", "admin"),
            ("Sunita Librarian", "librarian@library.com", "lib123", "librarian"),
            ("Aarav Student", "student@library.com", "student123", "student"),
            ("Faculty User", "faculty@library.com", "faculty123", "faculty"),
        ]
        for name,email,pwd,role in seed_users:
            conn.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
                         (name,email,generate_password_hash(pwd),role))
    books = conn.execute("SELECT COUNT(*) AS c FROM books").fetchone()["c"]
    if books == 0:
        sample = [
            ("Python Programming","Mark Lutz","Programming","9781449355739","A-01"),
            ("Artificial Intelligence","Stuart Russell","AI","9780134610993","A-02"),
            ("Clean Code","Robert C. Martin","Software Engineering","9780132350884","B-01"),
            ("Database System Concepts","Silberschatz","Database","9780073523323","B-02"),
            ("Computer Networks","Andrew S. Tanenbaum","Networking","9780132126953","C-01"),
        ]
        conn.executemany("INSERT INTO books(title,author,category,isbn,shelf) VALUES(?,?,?,?,?)", sample)
    conn.commit()
    conn.close()

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

def roles(*allowed):
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))
            if session.get("role") not in allowed:
                flash("You do not have permission for this action.", "danger")
                return redirect(url_for("dashboard"))
            return fn(*args, **kwargs)
        return wrapper
    return deco

@app.context_processor
def inject_user():
    return {"current_user": session.get("name"), "current_role": session.get("role")}

@app.route("/")
def index():
    return redirect(url_for("dashboard") if "user_id" in session else url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]
        conn = db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password"], password):
            session.update(user_id=user["id"], name=user["name"], role=user["role"])
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    conn = db()
    stats = {
        "books": conn.execute("SELECT COUNT(*) c FROM books").fetchone()["c"],
        "available": conn.execute("SELECT COUNT(*) c FROM books WHERE status='Available'").fetchone()["c"],
        "issued": conn.execute("SELECT COUNT(*) c FROM books WHERE status='Issued'").fetchone()["c"],
        "users": conn.execute("SELECT COUNT(*) c FROM users").fetchone()["c"],
    }
    if session["role"] in ("admin","librarian"):
        recent = conn.execute("""
            SELECT t.*, b.title, u.name FROM transactions t
            JOIN books b ON b.id=t.book_id JOIN users u ON u.id=t.user_id
            ORDER BY t.id DESC LIMIT 8
        """).fetchall()
    else:
        recent = conn.execute("""
            SELECT t.*, b.title FROM transactions t
            JOIN books b ON b.id=t.book_id WHERE t.user_id=?
            ORDER BY t.id DESC LIMIT 8
        """,(session["user_id"],)).fetchall()
    conn.close()
    return render_template("dashboard.html", stats=stats, recent=recent)

@app.route("/books")
@login_required
def books():
    q = request.args.get("q","").strip()
    conn = db()
    if q:
        like=f"%{q}%"
        rows=conn.execute("""SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ? OR category LIKE ? OR isbn LIKE ?
            ORDER BY title""",(like,like,like,like)).fetchall()
    else:
        rows=conn.execute("SELECT * FROM books ORDER BY title").fetchall()
    conn.close()
    return render_template("books.html", books=rows, q=q)

@app.route("/books/add", methods=["GET","POST"])
@roles("admin","librarian")
def add_book():
    if request.method=="POST":
        conn=db()
        conn.execute("""INSERT INTO books(title,author,category,isbn,shelf)
                        VALUES(?,?,?,?,?)""",
                     (request.form["title"],request.form["author"],request.form.get("category",""),
                      request.form.get("isbn",""),request.form.get("shelf","")))
        conn.commit(); conn.close()
        flash("Book added successfully.","success")
        return redirect(url_for("books"))
    return render_template("book_form.html", book=None)

@app.route("/books/delete/<int:book_id>", methods=["POST"])
@roles("admin","librarian")
def delete_book(book_id):
    conn=db()
    book=conn.execute("SELECT * FROM books WHERE id=?",(book_id,)).fetchone()
    if book and book["status"]=="Available":
        conn.execute("DELETE FROM books WHERE id=?",(book_id,))
        conn.commit(); flash("Book deleted.","success")
    else:
        flash("Only available books can be deleted.","danger")
    conn.close()
    return redirect(url_for("books"))

@app.route("/issue/<int:book_id>", methods=["GET","POST"])
@roles("admin","librarian","student","faculty")
def issue(book_id):
    conn=db()
    book=conn.execute("SELECT * FROM books WHERE id=?",(book_id,)).fetchone()
    if not book or book["status"]!="Available":
        conn.close(); flash("Book is not available.","danger"); return redirect(url_for("books"))
    if request.method=="POST":
        if session["role"] in ("admin","librarian"):
            user_id=int(request.form["user_id"])
        else:
            user_id=session["user_id"]
        issue_date=date.today()
        due=issue_date+timedelta(days=14)
        conn.execute("""INSERT INTO transactions(user_id,book_id,issue_date,due_date)
                        VALUES(?,?,?,?)""",(user_id,book_id,issue_date.isoformat(),due.isoformat()))
        conn.execute("UPDATE books SET status='Issued' WHERE id=?",(book_id,))
        conn.commit(); conn.close()
        flash(f"Book issued. Due date: {due.isoformat()}","success")
        return redirect(url_for("books"))
    users=conn.execute("SELECT id,name,email,role FROM users WHERE role IN ('student','faculty') ORDER BY name").fetchall()
    conn.close()
    return render_template("issue.html",book=book,users=users)

@app.route("/transactions")
@login_required
def transactions():
    conn=db()
    if session["role"] in ("admin","librarian"):
        rows=conn.execute("""SELECT t.*, b.title, u.name, u.email FROM transactions t
            JOIN books b ON b.id=t.book_id JOIN users u ON u.id=t.user_id ORDER BY t.id DESC""").fetchall()
    else:
        rows=conn.execute("""SELECT t.*, b.title, u.name, u.email FROM transactions t
            JOIN books b ON b.id=t.book_id JOIN users u ON u.id=t.user_id
            WHERE t.user_id=? ORDER BY t.id DESC""",(session["user_id"],)).fetchall()
    conn.close()
    return render_template("transactions.html",transactions=rows)

@app.route("/return/<int:transaction_id>", methods=["POST"])
@roles("admin","librarian")
def return_book(transaction_id):
    conn=db()
    t=conn.execute("SELECT * FROM transactions WHERE id=?",(transaction_id,)).fetchone()
    if not t or t["return_date"]:
        flash("Invalid transaction.","danger"); conn.close(); return redirect(url_for("transactions"))
    today=date.today()
    due=date.fromisoformat(t["due_date"])
    late=max(0,(today-due).days)
    fine=late*5.0
    conn.execute("UPDATE transactions SET return_date=?, fine=? WHERE id=?",(today.isoformat(),fine,transaction_id))
    conn.execute("UPDATE books SET status='Available' WHERE id=?",(t["book_id"],))
    conn.commit(); conn.close()
    flash(f"Book returned. Fine: ₹{fine:.2f}","success")
    return redirect(url_for("transactions"))

@app.route("/users")
@roles("admin")
def users():
    conn=db()
    rows=conn.execute("SELECT id,name,email,role FROM users ORDER BY name").fetchall()
    conn.close()
    return render_template("users.html",users=rows)

@app.route("/reports")
@roles("admin")
def reports():
    conn=db()
    data={
        "total_books":conn.execute("SELECT COUNT(*) c FROM books").fetchone()["c"],
        "issued":conn.execute("SELECT COUNT(*) c FROM books WHERE status='Issued'").fetchone()["c"],
        "total_users":conn.execute("SELECT COUNT(*) c FROM users").fetchone()["c"],
        "fines":conn.execute("SELECT COALESCE(SUM(fine),0) s FROM transactions").fetchone()["s"],
        "returned":conn.execute("SELECT COUNT(*) c FROM transactions WHERE return_date IS NOT NULL").fetchone()["c"],
    }
    categories=conn.execute("SELECT category, COUNT(*) c FROM books GROUP BY category ORDER BY c DESC").fetchall()
    conn.close()
    return render_template("reports.html",data=data,categories=categories)

@app.route("/health")
def health():
    return {"status":"ok","service":"library-management-platform"}

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
