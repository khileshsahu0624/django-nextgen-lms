# Django NextGen LMS

A modern, production-ready Learning Management System built with Django. This platform features a stunning glassmorphism frontend, passwordless OTP authentication, Role-Based Access Control (RBAC), and a premium SaaS-level admin dashboard with comprehensive analytics.

## ✨ Features

- **Modern UI/UX**: Premium frontend design featuring glassmorphism and modern CSS.
- **Secure Authentication**: Custom user model with passwordless OTP-based login (sent via terminal/email).
- **Role-Based Access Control (RBAC)**: Manage Students, Instructors, and Admin staff with precise permissions.
- **Enterprise Dashboard**: Built-in production-grade admin panel with Chart.js analytics, responsive sidebar, and data tables.
- **Fully RESTful API integrations**: Frontend modals communicate securely with Django backend via `fetch` API.

## 🚀 Quick Start Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/khileshsahu0624/django-nextgen-lms.git
   cd django-nextgen-lms
   ```

2. **Set up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup (MySQL required):**
   - Ensure MySQL is running and a database named `student_db` exists.
   - Run migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Navigate to `http://127.0.0.1:8000/` in your browser.

## 📁 Project Structure

- `accounts/` - Custom User authentication, OTP logic, API endpoints, and RBAC views.
- `website/` - Public frontend views and UI routing.
- `students/` - Student-specific logic and models.
- `templates/`
  - `user/` - Frontend HTML components (glassmorphism layouts, modals).
  - `admin/` - Premium backend dashboard HTML (sidebar, header, analytics).

## 🛠 Tech Stack
- **Backend:** Python, Django 4.2+
- **Database:** MySQL
- **Frontend:** HTML5, CSS3 Variables, Vanilla JS, FontAwesome
- **Analytics:** Chart.js
