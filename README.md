# 🏋️ Fitness CRM
<img width="1366" height="768" alt="Login" src="https://github.com/user-attachments/assets/8bf671cf-a806-40b6-8585-bf5dd498f966" />
<img width="1366" height="768" alt="dashboard" src="https://github.com/user-attachments/assets/e551cff0-19d4-401f-8fdf-c66c021c464b" />

A full-featured **Gym Management System** built with **Django** to help gym administrators manage members, memberships, attendance, trainers, payments, and reports through a modern and responsive dashboard.

The project is designed as a real-world management application with authentication, role-based access, membership tracking, attendance management, automated membership expiry checks, and a clean admin interface.

---

## 🚀 Features

### 👥 Member Management

* Add new gym members
* View member details
* Edit member information
* Search and manage members
* Track active/inactive members
* Manage membership history

### 💳 Membership Management

* Create and manage membership plans
* Assign memberships to members
* Set membership start and end dates
* Track active, expired, and upcoming memberships
* Renew memberships
* View membership history
* Automated membership expiry checking

### 🏃 Attendance Management

* Member check-in
* Member check-out
* Attendance history
* Today's attendance overview
* Attendance statistics
* Track member attendance records

### 🧑‍🏫 Trainer Management

* Add trainers
* Edit trainer information
* View trainer details
* Manage trainer records
* Integrate trainers with gym operations

### 💰 Payment Management

* Payment management structure
* Track membership-related payments
* Payment records associated with memberships
* Razorpay integration structure prepared for future implementation

### 📊 Dashboard & Reports

* Gym statistics dashboard
* Member statistics
* Membership statistics
* Attendance statistics
* Dashboard charts
* Reports and data summaries

### 🔐 Authentication & Authorization

* Django authentication
* Login/logout functionality
* Protected application pages
* Admin management
* Role-based access structure

### ⚙️ Background Tasks

* Celery integration
* Redis message broker
* Automated membership expiry checking
* Celery Beat scheduled tasks

### 🎨 Modern UI

* Responsive dashboard
* Tailwind CSS
* DaisyUI components
* Dark/Light mode support
* Orange-based primary theme
* Responsive sidebar navigation
* Clean management interfaces

---

## 🛠️ Tech Stack

| Technology        | Usage                      |
| ----------------- | -------------------------- |
| Python            | Programming language       |
| Django            | Backend web framework      |
| SQLite / Database | Data storage               |
| HTML5             | Frontend structure         |
| Tailwind CSS      | Styling                    |
| DaisyUI           | UI components              |
| JavaScript        | Frontend interactions      |
| Celery            | Background task processing |
| Redis             | Message broker             |
| Git               | Version control            |
| GitHub            | Source code hosting        |

---

## 📁 Project Structure

```text
gms/
│
├── accounts/
├── attendance/
├── config/
├── members/
├── memberships/
├── payments/
├── reports/
├── trainers/
│
├── templates/
│   ├── accounts/
│   ├── attendance/
│   ├── members/
│   ├── memberships/
│   ├── payments/
│   ├── reports/
│   ├── trainers/
│   └── includes/
│
├── static/
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

> **Note:** Sensitive files such as `.env` and the Python virtual environment should not be committed to the repository.

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Move into the project directory:

```bash
cd gms
```

---

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

Add any other environment variables required by your local configuration.

**Never commit your `.env` file to GitHub.**

---

### 5. Run migrations

```bash
python manage.py migrate
```

---

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create your administrator account.

---

### 7. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 🔄 Celery & Redis

The project uses **Celery** and **Redis** for background tasks.

Start Redis:

```bash
redis-server
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start the Celery worker:

```bash
celery -A config worker --loglevel=info
```

For scheduled tasks, start Celery Beat in another terminal:

```bash
celery -A config beat --loglevel=info
```

---

## 🔑 Admin Panel

After creating a superuser, access the Django administration panel:

```text
http://127.0.0.1:8000/admin/
```

Use the superuser credentials created with:

```bash
python manage.py createsuperuser
```
---

## 🔮 Future Improvements

Planned improvements include:

* [ ] Complete online payment integration
* [ ] Advanced role-based permissions
* [ ] More detailed financial reports
* [ ] Email notifications
* [ ] SMS notifications
* [ ] Membership renewal reminders
* [ ] Trainer scheduling
* [ ] Workout plan management
* [ ] Diet plan management
* [ ] REST API using Django REST Framework
* [ ] Mobile-friendly improvements
* [ ] Production deployment with Gunicorn and Nginx
* [ ] Cloud deployment on AWS

---

## 🧪 Development

Run Django's system checks:

```bash
python manage.py check
```

Run tests:

```bash
python manage.py test
```

---

## 🔒 Security

For production deployment:

* Set `DEBUG=False`
* Use a strong `SECRET_KEY`
* Store secrets in environment variables
* Configure `ALLOWED_HOSTS`
* Configure HTTPS
* Secure database credentials
* Configure secure cookies
* Never commit `.env` files or credentials

---

## 👨‍💻 Author

**Aldrin Jones**

Full-Stack Developer focused on **Python, Django, Django REST Framework, React, and modern web application development.**

---

## 📄 License

This project is currently intended for educational and portfolio purposes.

Add an appropriate open-source license if you decide to distribute the project publicly.
