# 📚 Book Store Web Application

A full-stack Book Store web application built using **Flask (Python)**, **MySQL**, and **HTML/CSS**.
This app allows users to browse books, add them to cart, and place orders, while admins can manage products.

---

## 🚀 Features

### 👤 User Features

* User Signup with OTP verification (Email)
* Secure Login (Password hashing)
* Browse available books
* Add books to cart
* View shopping cart
* Checkout using Razorpay
* Forgot Password with OTP

---

### 🛠️ Admin Features

* Admin Login
* Add new books
* View all books
* Delete books

---

## 🏗️ Tech Stack

* **Backend:** Flask (Python)
* **Database:** MySQL
* **Frontend:** HTML, CSS
* **Email Service:** SMTP (Gmail App Password)
* **Payment Integration:** Razorpay

---

## 📁 Project Structure

```
BOOK STORE/
│
├── app.py
├── templates/
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── admin_addproducts.html
│   ├── admin_manageproducts.html
│   ├── user_signup.html
│   ├── user_login.html
│   ├── user_home.html
│   ├── shopping_cart.html
│   ├── otpverify.html
│   ├── errorpage.html
│   └── forgot_password*.html
│
├── static/
│   └── images/
│       ├── logo.png
│       └── homeimage.png
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/YOUR_USERNAME/bookstore-app.git
cd bookstore-app
```

---

### 2️⃣ Install Dependencies

```
pip install flask pymysql
```

---

### 3️⃣ Setup MySQL Database

Create database:

```
CREATE DATABASE bookstore;
```

Create required tables (USERS, PRODUCTS, CART, ORDERS, ORDER_DETAILS)

---

### 4️⃣ Configure Database in `app.py`

```
db_config = {
    'host': 'localhost',
    'database': 'bookstore',
    'user': 'root',
    'password': 'yourpassword'
}
```

---

### 5️⃣ Setup Email (IMPORTANT)

* Enable **2-Step Verification**
* Generate **App Password**
* Set environment variables:

```
set EMAIL_USER=your_email@gmail.com
set EMAIL_PASS=your_app_password
```

---

### 6️⃣ Run Application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5006
```

---

## 💳 Payment Integration

* Uses Razorpay test key
* Can be replaced with live key for production

---

## 🔒 Security Features

* Password hashing using `werkzeug.security`
* Email-based OTP verification
* Secure database queries

---

## 📌 Notes

* Do NOT upload real passwords to GitHub
* Use environment variables for sensitive data
* This project is for learning/demo purposes

---

## 👨‍💻 Author

Mohan Krishna

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
