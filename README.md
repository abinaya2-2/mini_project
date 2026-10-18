# GuestSphere - Smart Guest Management & Event Attendance Tracking System

An MCA mini-project: a full-stack Flask web app for managing events, guests,
RSVPs, invitations, QR code check-in, face-recognition check-in, seating,
reports, and notifications from a single admin dashboard.

## 1. Features

- Admin/staff authentication (hashed passwords, sessions, role-based access)
- Event CRUD with capacity, venue, date/time, status
- Guest CRUD with search, filter, pagination
- Invitation links + RSVP accept/decline flow (public page, no login needed)
- Unique signed QR code per guest, webcam QR scanning, duplicate check-in prevention
- Real OpenCV LBPH face registration & recognition (webcam based)
- Seating plan with tables, capacity, VIP tables
- Dashboard with live stats + RSVP chart + recent activity feed
- CSV and PDF report export (guests, attendance)
- In-app notifications (RSVP received, check-in, invitation sent, etc.)
- Activity log / audit trail

## 2. Technology Stack

- Frontend: HTML5, CSS3, Bootstrap 5, Font Awesome, vanilla JS
- Backend: Python 3, Flask, Flask-Login
- Database: SQLAlchemy ORM - MySQL (production) or SQLite (zero-setup demo)
- Face Recognition: OpenCV + LBPH
- QR Codes: `qrcode` (generation) + `jsQR` (browser-side scanning)
- Reports: ReportLab (PDF), built-in `csv` module

## 3. System Requirements

- Python 3.10+
- pip
- A webcam (for QR/face check-in features)
- MySQL 8+ (optional - only needed if you want to use MySQL instead of the
  default SQLite database)

## 4. Installation

```bash
# 1. Clone / extract the project, then enter the folder
cd GuestSphere

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

> **Note on OpenCV:** `opencv-contrib-python` (required for `cv2.face.LBPHFaceRecognizer_create`)
> is a large package. If installation fails on your machine, see the
> Troubleshooting section below.

## 5. Environment Variables

Copy `.env.example` to `.env` and fill in real values:

```bash
cp .env.example .env
```

At minimum, set a real `SECRET_KEY` and `QR_SECRET_SALT`. Leave `DATABASE_URL`
unset to use the bundled SQLite database, or set it to a MySQL URL (see
below) for a production-style setup.

## 6. MySQL Database Setup (optional - full production setup)

```sql
CREATE DATABASE guestsphere CHARACTER SET utf8mb4;
CREATE USER 'guestsphere_user'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON guestsphere.* TO 'guestsphere_user'@'localhost';
FLUSH PRIVILEGES;
```

Then in `.env`:

```
DATABASE_URL=mysql+pymysql://guestsphere_user:yourpassword@localhost:3306/guestsphere
```

You can create the tables either via SQLAlchemy (`python init_db.py`, which
also seeds demo data) or manually with the provided `schema.sql`:

```bash
mysql -u guestsphere_user -p guestsphere < schema.sql
```

If you load `schema.sql` manually, still run `python init_db.py` afterwards
so the demo admin/guest data gets seeded (it detects existing tables and
skips `create_all`, then seeds data only if the admin account is missing).

## 7. Database Initialization (SQLite quick-start)

If you just want to run the project immediately without installing MySQL:

```bash
python init_db.py
```

This creates `guestsphere.db` (SQLite) in the project folder and seeds:
- 1 admin user
- 2 events
- 8 guests with a mix of RSVP statuses
- sample invitations, attendance records, seating assignments, notifications

## 8. Running the Application

```bash
python app.py
```

Visit **http://localhost:5000** in your browser.

## 9. Default Demo Login

```
Email:    admin@guestsphere.com
Password: Admin@123
```

## 10. QR Check-in Setup

1. Guests automatically get a QR code generated (containing a signed,
   opaque token - never their raw email/name) when they're added.
2. Go to **QR Check-in** in the sidebar, click "Start Camera", and allow
   browser camera access.
3. Point a guest's downloaded/printed QR code at the camera. It's scanned
   client-side with `jsQR` and verified server-side; duplicate check-ins are
   rejected automatically.

## 11. Face Recognition Setup

1. Open a guest's detail page and click **Register Face**.
2. Allow camera access, then click "Capture Sample" 5 times from slightly
   different angles/expressions.
3. Click "Finish & Train" - this retrains the shared LBPH model using every
   guest's stored samples.
4. Go to **Face Recognition** in the sidebar to run live check-in - the
   camera captures a frame, the backend runs face detection + LBPH
   prediction, and checks the guest in automatically if the confidence
   score is below the configured threshold (`FACE_RECOGNITION_CONFIDENCE_THRESHOLD`
   in `.env`, default 70 - lower is a stricter/better match in LBPH).

This is a genuine working implementation, not a placeholder: it depends on
`opencv-contrib-python` being installed and a working webcam/browser camera
permission.

## 12. Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: cv2` | Run `pip install opencv-contrib-python` (not the plain `opencv-python` package - it lacks `cv2.face`). |
| Face recognition endpoints return 500 "OpenCV is not installed" | Same as above - reinstall `opencv-contrib-python` inside your active virtualenv. |
| Camera doesn't open in the browser | Camera access requires HTTPS or `localhost`. Also check OS-level camera permissions for your browser. |
| `sqlalchemy.exc.OperationalError` connecting to MySQL | Check `DATABASE_URL` credentials/host/port, and that the MySQL server is running and the database exists. |
| Login fails after `pip install` | Run `python init_db.py` first to create the demo admin account. |
| QR image missing/404 on guest page | The `uploads/` folder is created automatically on first run; make sure the app has write permission to the project directory. |

## 13. Project Structure

```
GuestSphere/
├── app.py                # App factory + entry point
├── config.py              # Env-based configuration
├── init_db.py              # DB init + demo data seeding
├── requirements.txt
├── .env.example
├── schema.sql              # MySQL schema (manual setup option)
├── models/                 # SQLAlchemy models
├── routes/                 # Flask blueprints (one per module)
├── services/                # QR, face recognition, reports, notifications
├── templates/               # Jinja2 templates
├── static/{css,js,images}/
├── face_data/                # Captured face sample images (per guest)
├── models_data/               # Trained LBPH model file
├── uploads/                    # Generated QR code images
└── tests/                       # Basic automated tests
```

## 14. Testing

Automated tests (pytest):

```bash
pip install pytest
pytest tests/
```

### Manual Testing Checklist

1. Log in with the demo admin account.
2. Create a new event, edit it, confirm it appears in the events list.
3. Add a new guest to that event; confirm a QR code image is generated.
4. Open the guest's invitation link (find it in the server console log after
   clicking "Send Invitation" - dev mode logs it instead of emailing) and
   accept/decline the RSVP; confirm the guest list and dashboard update.
5. Use QR Check-in to scan the guest's downloaded QR code; confirm
   attendance is recorded and a second scan is rejected as a duplicate.
6. Register a guest's face, then use Face Recognition check-in to verify
   they're recognized and checked in.
7. Create a seating table and assign a guest to it.
8. Export a Guest Report and an Attendance Report (CSV and PDF).
9. Check that notifications appear for RSVP/check-in/invitation events.

## 15. Security Notes

- Passwords are hashed with Werkzeug's `generate_password_hash` (never
  stored in plaintext).
- All secrets (`SECRET_KEY`, `QR_SECRET_SALT`, DB credentials) are read from
  environment variables via `.env` - never hardcoded.
- QR codes encode a random opaque token plus a salted signature, not guest
  PII, and are verified server-side before any check-in is recorded.
- All database queries go through SQLAlchemy's ORM (parameterized), which
  protects against SQL injection.
- Sessions are managed by Flask-Login; protected routes require
  `@login_required` and unauthenticated access redirects to `/login`.

## 16. Project Completion Checklist

- [x] Authentication
- [x] Dashboard
- [x] Event Management
- [x] Guest Management
- [x] RSVP
- [x] Invitations
- [x] QR Check-in
- [x] Face Recognition
- [x] Seating Plan
- [x] Reports
- [x] Notifications
- [x] Settings
- [x] MySQL-compatible Database (SQLAlchemy, `schema.sql` provided)
- [x] Security (hashed passwords, env config, ORM, signed QR tokens)
- [x] Testing (automated + manual checklist)
- [x] README
