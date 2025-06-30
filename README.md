# 🛒 Grocery Store Management System

This is a **desktop-based Grocery Store Management System** built using **Python (Django + Tkinter)** and **MySQL**. 
It helps administrators manage stock, employees, sales, and billing efficiently through a modern UI with light/dark mode support.

---

## 🔧 Features

- 🔐 Authentication system (Login & Register)
- 📦 Stock Management (Add, update, delete items)
- 👨‍💼 Employee Management
- 💰 Sales & Profit analysis with charts
- 🧾 Invoice/Billing generation (Print-friendly)
- 🎨 Light/Dark Mode Toggle
- 🔍 Search & Filter for quick access

---

## 🛠 Technologies Used

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Database**: MySQL
- **UI**: Tkinter (for local GUI), Bootstrap-inspired CSS
- **Auth**: Django built-in user system with hashed passwords

---

## 💻 Installation (For Contributors & Users)

> Ensure you have Python 3.10+ and MySQL installed on your system.

### ✅ Prerequisites

- Python 3.10 or higher
- MySQL Server & Client
- Git

Please read **requirements.txt** file for more information on project set-up and initalization.

### 🔽 Clone the Repository

```bash
git clone https://github.com/Yash-775/Grocery-Store-Management.git
cd grocery_store
```

### 🗂️ Create Virtual Environment & Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 🗄️ Database Setup

- Create a MySQL database
grocery_db

- Update settings.py
Add your MySQL credentials in the DATABASES section.

- Run Migrations & Create Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
- Run the Development Server

```bash
python manage.py runserver
```

### 🤝 Contributing 
Pull requests are welcome!
If you’d like to contribute, please fork the repo and use a feature branch.
Don’t forget to add your changes with clear commit messages.

### 📄 License 
This project is licensed under the MIT License.
See the **LICENSE** file for full details.

### 🛡️ Security & Privacy 
No sensitive or personal data is stored in this repository.
Always ensure you keep your local **settings.py** credentials safe and out of version control.

### 📸 Screenshot of the Project 

- Login & Registeration Page 
![image](https://github.com/user-attachments/assets/a39ead74-5af8-488c-b0f4-63b0f1778daa)
![image](https://github.com/user-attachments/assets/ac77866c-1a8d-4157-bf13-f8e6d07a7882)

- Dashboard Home 
![image](https://github.com/user-attachments/assets/0122be37-e91a-4c64-adda-a8147a4301f3)

- Analytics Section 
![image](https://github.com/user-attachments/assets/a10ff46d-4327-45c8-b855-5974a626de3b)

- Manage Stock Section 
![image](https://github.com/user-attachments/assets/041e5a0a-d9d5-43d1-b0d2-0bc604f387c9)

- Employees Section 
![image](https://github.com/user-attachments/assets/5de0656f-5341-455f-b9cf-73b646939b02)

- Sales & Profit Section 
![image](https://github.com/user-attachments/assets/70de96b9-3b35-49f8-b9ab-499b945f4854)

- Billing Application (Tkinter GUI)

![image](https://github.com/user-attachments/assets/07bf4f8e-e7c6-4a55-b85f-8c66dead9600)

- View Bills/ Orders Section 
![image](https://github.com/user-attachments/assets/e8b402d8-7ea5-4ff5-9bf6-88b0923700e1)

- Print Recipts 
![image](https://github.com/user-attachments/assets/4858518e-b717-4850-b028-73a976791c01)
![image](https://github.com/user-attachments/assets/c262a0e5-6f3c-4be2-b0b0-e886468d71c4)

Thank you for viewing the project.






