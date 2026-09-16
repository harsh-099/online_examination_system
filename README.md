# 📝 Online Examination System

A web-based **Online Examination System** developed using Django to conduct and manage online examinations efficiently.

The system provides a platform for students to register, log in, attend online examinations, answer questions, and view their results.

---

## 🌐 Project Overview

The **Online Examination System** is designed to digitize the traditional examination process.

It provides a user-friendly interface for students to participate in online exams while allowing examination data, questions, students, and results to be managed through the system.

---

## ✨ Features

- 👨‍🎓 Student registration and login
- 🔐 Secure user authentication
- 📝 Online examination system
- ❓ Multiple-choice questions
- ⏱️ Exam timer
- 💾 Save and Next question navigation
- 🟢 Attempted question indication
- 📊 Automatic result calculation
- 📋 Student result management
- 👤 Student profile management
- 📷 Student profile photo upload
- 🎥 Camera image capture during registration
- 🔎 Exam and question management
- 📱 Responsive user interface
- 🛡️ Authentication and access control
- ⚙️ Django admin panel

---

## 🧩 Main Modules

| Module | Description |
|---|---|
| 👨‍🎓 Student | Student registration, login and profile management |
| 📝 Examination | Online exam and question management |
| ❓ Questions | Manage examination questions and answers |
| ⏱️ Exam Timer | Controls examination time |
| 📊 Results | Calculates and displays examination results |
| 👤 Profile | Manage student profile information and photo |
| 🔐 Authentication | Login, registration and access control |
| ⚙️ Admin Panel | Manage students, exams, questions and results |

---

## 🛠️ Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap

### Backend

- Python
- Django

### Database

- SQLite

### Tools

- Git
- GitHub
- VS Code

---

## 🗂️ Project Structure

```text
online_examination_system/
│
├── exam/
├── student/
├── onlinexam/
│
├── templates/
├── static/
├── media/
│
├── db.sqlite3
├── manage.py
├── requirements.txt
├── LICENSE
└── README.md
```



## ▶️ How to Run

1. **Clone the repo**:
```bash
git clone https: https://github.com/harsh-099/online_examination_system.git
cd online_examination_system
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```
3. **Apply database migrations**:
```bash
python manage.py migrate
```

4. **Create a superuser**:
```bash
python manage.py createsuperuser
```

5.**Run the development server**:
```bash
python manage.py runserver
```

6.**Open the application**:
```bash
http://127.0.0.1:8000/
```

7.**Django Admin Panel**:
```bash
http://127.0.0.1:8000/admin/
```


**🎯 Project Objectives**

#The main goals of this project are:
- Digitize traditional examination process
- Reduce manual examination work
- Provide an online platform for conducting exams
- Automate result calculation
- Improve examination management
- Provide a simple and responsive student interface
- Maintain student and examination records efficiently



**🔐 Security & Authentication**

The system includes authentication and access control mechanisms to ensure that:
- Students can access their authorized pages
- Unauthenticated users cannot access protected examination pages
- Student accounts are securely managed
- Examination-related data is controlled through Django

**🚀 Future Enhancements**
- 📧 Email notifications
- 📄 PDF result generation
- 📊 Advanced performance analytics
- 🏆 Student ranking and leaderboard
- 🔔 Exam notifications
- 🗃️ MySQL / PostgreSQL database integration
- ☁️ Cloud deployment
- 👨‍🏫 Advanced teacher dashboard
- 📈 Detailed student performance reports


## 🤝 Contribution

Contributions, suggestions, and improvements are welcome.

If you would like to contribute:

- Fork the repository
- Create a new branch
- Make your changes
- Commit your changes
- Submit a Pull Request

## 📬 Contact

Made with ❤️ by Harshnil Patil

Connect on LinkedIn https://www.linkedin.com/in/harshnilpatil/
