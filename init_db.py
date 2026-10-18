"""
Database initialization + demo data seeding script.
Run once after setting up your .env: `python init_db.py`
Safe to re-run - it checks for existing data before seeding.
"""
from datetime import date, time, datetime, timedelta

from app import create_app
from models import (
    db, User, Event, Guest, RSVP, Invitation, Attendance,
    SeatingTable, SeatingAssignment, Notification,
)
from services.qr_service import generate_qr_for_guest

app = create_app()


def seed():
    with app.app_context():
        db.create_all()
        print("Tables created (or already exist).")

        if User.query.filter_by(email="admin@guestsphere.com").first():
            print("Demo data already present - skipping seed.")
            return

        # --- Admin user ---
        admin = User(full_name="Admin User", email="admin@guestsphere.com", role="admin")
        admin.set_password("Admin@123")
        db.session.add(admin)
        db.session.commit()
        print("Created admin login: admin@guestsphere.com / Admin@123")

        # --- Events ---
        event1 = Event(
            name="Annual Tech Conference 2026",
            description="A full-day conference on emerging technology trends.",
            event_date=date.today() + timedelta(days=14),
            start_time=time(9, 0),
            end_time=time(17, 0),
            venue="Grand Convention Center, Hall A",
            capacity=200,
            status="upcoming",
            created_by=admin.id,
        )
        event2 = Event(
            name="Alumni Meetup",
            description="Casual evening networking event for MCA alumni.",
            event_date=date.today() - timedelta(days=5),
            start_time=time(18, 0),
            end_time=time(21, 0),
            venue="Campus Auditorium",
            capacity=80,
            status="completed",
            created_by=admin.id,
        )
        db.session.add_all([event1, event2])
        db.session.commit()

        # --- Guests ---
        demo_guests = [
            ("Aarav Sharma", "aarav.sharma@example.com", "9876500001", "accepted", event1),
            ("Diya Nair", "diya.nair@example.com", "9876500002", "pending", event1),
            ("Rohan Mehta", "rohan.mehta@example.com", "9876500003", "declined", event1),
            ("Ishita Rao", "ishita.rao@example.com", "9876500004", "accepted", event1),
            ("Kabir Singh", "kabir.singh@example.com", "9876500005", "pending", event1),
            ("Ananya Iyer", "ananya.iyer@example.com", "9876500006", "accepted", event2),
            ("Vikram Joshi", "vikram.joshi@example.com", "9876500007", "accepted", event2),
            ("Sneha Pillai", "sneha.pillai@example.com", "9876500008", "pending", event2),
        ]

        guests = []
        for name, email, phone, rsvp_status, event in demo_guests:
            guest = Guest(
                event_id=event.id,
                full_name=name,
                email=email,
                phone=phone,
                organization="Demo Org",
                rsvp_status=rsvp_status,
            )
            db.session.add(guest)
            db.session.flush()
            db.session.add(RSVP(guest_id=guest.id, event_id=event.id, status=rsvp_status))
            guests.append(guest)
        db.session.commit()

        # Generate QR codes now that guests have IDs
        for guest in guests:
            generate_qr_for_guest(guest)

        # --- Invitations ---
        for guest in guests:
            db.session.add(Invitation(guest_id=guest.id, status="sent" if guest.rsvp_status == "pending" else "responded"))
        db.session.commit()

        # --- Sample attendance for accepted guests at the past event ---
        for guest in guests:
            if guest.rsvp_status == "accepted" and guest.event_id == event2.id:
                guest.checkin_status = True
                db.session.add(Attendance(guest_id=guest.id, event_id=event2.id, method="manual"))
        db.session.commit()

        # --- Seating for event1 ---
        table1 = SeatingTable(event_id=event1.id, table_name="Table 1", capacity=6, is_vip=True)
        table2 = SeatingTable(event_id=event1.id, table_name="Table 2", capacity=6, is_vip=False)
        db.session.add_all([table1, table2])
        db.session.commit()

        accepted_event1_guests = [g for g in guests if g.event_id == event1.id and g.rsvp_status == "accepted"]
        if accepted_event1_guests:
            db.session.add(SeatingAssignment(table_id=table1.id, guest_id=accepted_event1_guests[0].id))
            db.session.commit()

        # --- Notifications ---
        db.session.add_all([
            Notification(title="Welcome to GuestSphere", message="Your account is set up and ready to go.", category="general"),
            Notification(title="New RSVP Received", message="Aarav Sharma accepted the invitation.", category="rsvp"),
            Notification(title="Event Reminder", message="Annual Tech Conference 2026 is coming up in 14 days.", category="reminder"),
        ])
        db.session.commit()

        print("Demo data seeded successfully:")
        print(f"  - {Event.query.count()} events")
        print(f"  - {Guest.query.count()} guests")
        print(f"  - {Invitation.query.count()} invitations")
        print(f"  - {Attendance.query.count()} attendance records")


if __name__ == "__main__":
    seed()
