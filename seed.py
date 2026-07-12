"""
Seed script – populates the EcoSphere SQLite database with realistic demo data.
Run from the project root:
    python seed.py
"""
import asyncio
import uuid
from datetime import datetime, timedelta, timezone
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from database.session import async_session_maker, engine
from models.base import Base
from models.user import User
from models.department import Department
from models.category import Category
from models.emission_factor import EmissionFactor
from models.carbon_transaction import CarbonTransaction
from models.csr_activity import CSRActivity
from models.challenge import Challenge
from models.challenge_participation import ChallengeParticipation
from models.compliance_issue import ComplianceIssue
from models.department_score import DepartmentScore
from models.goal import Goal
from models.notification import Notification
from models.policy import Policy
from models.badge import Badge
from models.reward import Reward
from security.password import get_password_hash
from sqlalchemy import text

def now(): return datetime.now(timezone.utc)
def daysago(n): return now() - timedelta(days=n)
def uid(): return uuid.uuid4()


async def seed():
    print("🌱 Seeding EcoSphere database...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as db:
        # ── Departments ──────────────────────────────────────────────────────
        dept_ids = {
            "engineering":  uid(), "marketing":    uid(),
            "operations":   uid(), "hr":           uid(),
            "finance":      uid(), "sustainability": uid(),
        }
        departments = [
            Department(id=dept_ids["engineering"],   name="Engineering",   code="ENG",  description="Software & infrastructure teams",   status="active"),
            Department(id=dept_ids["marketing"],     name="Marketing",     code="MKT",  description="Brand and communications",          status="active"),
            Department(id=dept_ids["operations"],    name="Operations",    code="OPS",  description="Supply chain and logistics",        status="active"),
            Department(id=dept_ids["hr"],            name="Human Resources", code="HR", description="People and culture",               status="active"),
            Department(id=dept_ids["finance"],       name="Finance",       code="FIN",  description="Accounting and FP&A",              status="active"),
            Department(id=dept_ids["sustainability"],name="Sustainability", code="SUS", description="ESG strategy and reporting",       status="active"),
        ]
        db.add_all(departments)
        await db.flush()

        # ── Users ────────────────────────────────────────────────────────────
        user_ids = {k: uid() for k in ["alice", "bob", "carol", "dave", "eve", "frank"]}
        users = [
            User(id=user_ids["alice"], email="alice@ecosphere.com",  full_name="Alice Chen",    role="admin",    department_id=dept_ids["sustainability"], points=1250, hashed_password=get_password_hash("password123")),
            User(id=user_ids["bob"],   email="bob@ecosphere.com",    full_name="Bob Patel",     role="manager",  department_id=dept_ids["engineering"],    points=980,  hashed_password=get_password_hash("password123")),
            User(id=user_ids["carol"], email="carol@ecosphere.com",  full_name="Carol Santos",  role="employee", department_id=dept_ids["marketing"],      points=760,  hashed_password=get_password_hash("password123")),
            User(id=user_ids["dave"],  email="dave@ecosphere.com",   full_name="Dave Kim",      role="employee", department_id=dept_ids["operations"],     points=540,  hashed_password=get_password_hash("password123")),
            User(id=user_ids["eve"],   email="eve@ecosphere.com",    full_name="Eve Johnson",   role="manager",  department_id=dept_ids["hr"],             points=820,  hashed_password=get_password_hash("password123")),
            User(id=user_ids["frank"], email="frank@ecosphere.com",  full_name="Frank Müller",  role="employee", department_id=dept_ids["finance"],        points=410,  hashed_password=get_password_hash("password123")),
        ]
        db.add_all(users)
        await db.flush()

        # ── Categories ───────────────────────────────────────────────────────
        cat_ids = {k: uid() for k in ["energy", "transport", "waste", "water", "supply"]}
        categories = [
            Category(id=cat_ids["energy"],    name="Energy",          description="Electricity and heating emissions",   status="active"),
            Category(id=cat_ids["transport"], name="Transport",       description="Business travel and fleet",           status="active"),
            Category(id=cat_ids["waste"],     name="Waste",           description="Landfill and recycling",              status="active"),
            Category(id=cat_ids["water"],     name="Water",           description="Water consumption and treatment",     status="active"),
            Category(id=cat_ids["supply"],    name="Supply Chain",    description="Scope 3 upstream emissions",          status="active"),
        ]
        db.add_all(categories)
        await db.flush()

        # ── Emission Factors ─────────────────────────────────────────────────
        efs = [
            EmissionFactor(id=uid(), name="UK Grid Electricity",      category_id=cat_ids["energy"],    factor_value=0.233, unit="kg CO2e/kWh",   source="DEFRA 2023", status="active"),
            EmissionFactor(id=uid(), name="Natural Gas",              category_id=cat_ids["energy"],    factor_value=0.202, unit="kg CO2e/kWh",   source="DEFRA 2023", status="active"),
            EmissionFactor(id=uid(), name="Petrol Car (avg)",         category_id=cat_ids["transport"], factor_value=0.171, unit="kg CO2e/km",    source="DEFRA 2023", status="active"),
            EmissionFactor(id=uid(), name="Short-haul Flight",        category_id=cat_ids["transport"], factor_value=0.255, unit="kg CO2e/km",    source="DEFRA 2023", status="active"),
            EmissionFactor(id=uid(), name="Landfill Waste",           category_id=cat_ids["waste"],     factor_value=0.587, unit="kg CO2e/kg",    source="DEFRA 2023", status="active"),
            EmissionFactor(id=uid(), name="Water Supply & Treatment", category_id=cat_ids["water"],     factor_value=0.344, unit="kg CO2e/m3",    source="DEFRA 2023", status="active"),
        ]
        db.add_all(efs)
        await db.flush()

        # ── Carbon Transactions (6 months of data) ───────────────────────────
        sources = ["Electricity (HQ)", "Data Centre Energy", "Employee Commute", "Business Air Travel",
                   "Waste Disposal", "Water Usage", "Renewable PPA Offset", "Tree Planting Credits",
                   "Carbon Credit Purchase", "Solar Generation Offset"]
        txns = []
        for month_offset in range(6):
            base_date = daysago(150 - month_offset * 25)
            for i, user_key in enumerate(user_ids.values()):
                # Debits (emissions)
                txns.append(CarbonTransaction(
                    id=uid(), user_id=user_key,
                    amount=round(4200 - month_offset * 300 + i * 120, 2),
                    type="debit", source=sources[i % 6],
                    date=base_date + timedelta(days=i),
                    notes="Monthly emission record", status="active"
                ))
                # Credits (offsets)
                txns.append(CarbonTransaction(
                    id=uid(), user_id=user_key,
                    amount=round(2400 + month_offset * 280 + i * 50, 2),
                    type="credit", source=sources[(i + 6) % 10],
                    date=base_date + timedelta(days=i + 5),
                    notes="Offset credit", status="active"
                ))
        db.add_all(txns)

        # ── CSR Activities ───────────────────────────────────────────────────
        csr_activities = [
            CSRActivity(id=uid(), title="Community Tree Planting Drive",      description="Staff volunteered 3 hours planting 200 native trees in the local park.",    date=daysago(30),  department_id=dept_ids["sustainability"], points=300, status="approved"),
            CSRActivity(id=uid(), title="E-Waste Collection Campaign",         description="Collected 450 kg of e-waste from local businesses for certified recycling.", date=daysago(45),  department_id=dept_ids["operations"],     points=250, status="approved"),
            CSRActivity(id=uid(), title="STEM Workshop for Schools",           description="Hosted 3 interactive STEM sessions for local secondary school students.",    date=daysago(60),  department_id=dept_ids["hr"],             points=200, status="approved"),
            CSRActivity(id=uid(), title="Biodiversity Audit of Office Grounds",description="Full survey of flora and fauna on company property.",                         date=daysago(20),  department_id=dept_ids["engineering"],    points=150, status="pending"),
            CSRActivity(id=uid(), title="Solar Panel Installation",            description="Installed 80 kW solar array on warehouse roof.",                              date=daysago(90),  department_id=dept_ids["finance"],        points=500, status="approved"),
            CSRActivity(id=uid(), title="Supplier Sustainability Audit",       description="On-site audits of top 10 suppliers against ESG framework.",                   date=daysago(15),  department_id=dept_ids["sustainability"], points=400, status="pending"),
        ]
        db.add_all(csr_activities)

        # ── Challenges ────────────────────────────────────────────────────────
        challenge_ids = [uid(), uid(), uid(), uid()]
        challenges = [
            Challenge(id=challenge_ids[0], title="Zero-Waste Lunch Week",       description="Bring a waste-free lunch every day for a week. No single-use plastic!", start_date=daysago(10), end_date=daysago(-20), goal="Zero plastic waste for 5 days", points=150, status="active"),
            Challenge(id=challenge_ids[1], title="Cycle to Work Month",         description="Cycle or walk to work instead of driving for the entire month.",         start_date=daysago(5),  end_date=daysago(-25), goal="Use active transport daily",    points=200, status="active"),
            Challenge(id=challenge_ids[2], title="Energy Saving Challenge",     description="Reduce your team's energy consumption by 15% vs last month.",            start_date=daysago(30), end_date=daysago(-1),  goal="15% energy reduction",          points=300, status="active"),
            Challenge(id=challenge_ids[3], title="Paperless Office Q2",         description="Go completely paperless – digitise all workflows and documents.",         start_date=daysago(90), end_date=daysago(-5),  goal="100% digital workflows",        points=250, status="completed"),
        ]
        db.add_all(challenges)

        # ── Challenge Participations ──────────────────────────────────────────
        participations = []
        for user_key in [user_ids["alice"], user_ids["bob"], user_ids["carol"]]:
            participations.append(ChallengeParticipation(id=uid(), challenge_id=challenge_ids[0], user_id=user_key, status="active",    progress=75.0))
            participations.append(ChallengeParticipation(id=uid(), challenge_id=challenge_ids[1], user_id=user_key, status="active",    progress=60.0))
        participations.append(ChallengeParticipation(id=uid(), challenge_id=challenge_ids[3], user_id=user_ids["dave"],  status="completed", progress=100.0))
        participations.append(ChallengeParticipation(id=uid(), challenge_id=challenge_ids[3], user_id=user_ids["eve"],   status="completed", progress=100.0))
        db.add_all(participations)

        # ── Compliance Issues ────────────────────────────────────────────────
        issues = [
            ComplianceIssue(id=uid(), description="GHG inventory not updated for Q4 2024. Scope 2 figures are missing.",                       severity="high",     status="open"),
            ComplianceIssue(id=uid(), description="Supplier X has not submitted annual ESG disclosure for 2024.",                               severity="medium",   status="open"),
            ComplianceIssue(id=uid(), description="Refrigerant leak detected in server room – F-gas reporting required.",                       severity="critical", status="open"),
            ComplianceIssue(id=uid(), description="Employee data retention policy expired. GDPR breach risk.",                                  severity="high",     status="open"),
            ComplianceIssue(id=uid(), description="Fire safety certificate renewal overdue by 30 days.",                                        severity="medium",   status="open"),
            ComplianceIssue(id=uid(), description="Annual water usage report submitted 10 days late.",                                          severity="low",      status="resolved"),
            ComplianceIssue(id=uid(), description="Carbon offset certificates verified and filed.",                                             severity="low",      status="resolved"),
        ]
        db.add_all(issues)

        # ── Department Scores (last 6 months) ────────────────────────────────
        dept_score_configs = {
            "engineering":   [72, 75, 78, 80, 82, 85],
            "marketing":     [65, 67, 69, 70, 71, 73],
            "operations":    [80, 83, 85, 87, 89, 90],
            "hr":            [78, 80, 82, 83, 85, 88],
            "finance":       [60, 63, 65, 68, 70, 72],
            "sustainability":[85, 87, 89, 90, 92, 94],
        }
        scores = []
        current_month = now().month
        current_year  = now().year
        for dept_key, score_list in dept_score_configs.items():
            for i, score_val in enumerate(score_list):
                month = ((current_month - 6 + i) % 12) or 12
                year  = current_year if month <= current_month else current_year - 1
                scores.append(DepartmentScore(
                    id=uid(), department_id=dept_ids[dept_key],
                    score=float(score_val), month=month, year=year, status="active"
                ))
        db.add_all(scores)

        # ── Goals ────────────────────────────────────────────────────────────
        goals = [
            Goal(id=uid(), name="Net Zero Carbon Emissions 2030",           description="Achieve net-zero across Scopes 1, 2, and 3 by 2030.",       target_value=0.0,     current_value=12400.0, unit="tCO2e",   deadline=datetime(2030, 12, 31, tzinfo=timezone.utc), department_id=dept_ids["sustainability"], status="on_track"),
            Goal(id=uid(), name="50% Renewable Energy by 2025",             description="Source half of all electricity from renewables.",             target_value=50.0,    current_value=38.5,    unit="%",       deadline=datetime(2025, 12, 31, tzinfo=timezone.utc), department_id=dept_ids["engineering"],    status="on_track"),
            Goal(id=uid(), name="Zero Single-Use Plastic by Q3 2025",       description="Eliminate single-use plastics from all offices.",             target_value=0.0,     current_value=2.1,     unit="kg/week", deadline=datetime(2025, 9, 30, tzinfo=timezone.utc),  department_id=dept_ids["operations"],    status="at_risk"),
            Goal(id=uid(), name="30% Supply Chain Emissions Reduction",     description="Cut Scope 3 upstream supply chain emissions by 30%.",         target_value=30.0,    current_value=11.2,    unit="%",       deadline=datetime(2026, 6, 30, tzinfo=timezone.utc),  department_id=dept_ids["sustainability"], status="on_track"),
            Goal(id=uid(), name="Employee ESG Training 100%",               description="Ensure all employees complete ESG awareness training.",        target_value=100.0,   current_value=74.0,    unit="%",       deadline=datetime(2025, 6, 30, tzinfo=timezone.utc),  department_id=dept_ids["hr"],            status="on_track"),
            Goal(id=uid(), name="Water Usage Reduction 20%",                description="Reduce total water consumption by 20% vs 2022 baseline.",     target_value=20.0,    current_value=9.5,     unit="%",       deadline=datetime(2025, 12, 31, tzinfo=timezone.utc), department_id=dept_ids["operations"],    status="at_risk"),
        ]
        db.add_all(goals)

        # ── Policies ─────────────────────────────────────────────────────────
        policies = [
            Policy(id=uid(), title="Environmental Management Policy",     version="3.1", status="active"),
            Policy(id=uid(), title="Supplier Code of Conduct",            version="2.0", status="active"),
            Policy(id=uid(), title="Data Privacy & Retention Policy",     version="4.2", status="active"),
            Policy(id=uid(), title="Anti-Bribery & Corruption Policy",    version="1.5", status="active"),
            Policy(id=uid(), title="Health & Safety Framework",           version="5.0", status="active"),
            Policy(id=uid(), title="Carbon Reporting Standard (Archived)",version="1.0", status="inactive"),
        ]
        db.add_all(policies)

        # ── Badges ───────────────────────────────────────────────────────────
        badges = [
            Badge(id=uid(), name="Green Pioneer",      description="First to log a carbon offset",      status="active"),
            Badge(id=uid(), name="Challenge Champion", description="Completed 5 sustainability challenges", status="active"),
            Badge(id=uid(), name="CSR Hero",           description="Participated in 10 CSR activities", status="active"),
            Badge(id=uid(), name="Net Zero Warrior",   description="Department achieved monthly net zero", status="active"),
        ]
        db.add_all(badges)

        # ── Rewards ──────────────────────────────────────────────────────────
        rewards = [
            Reward(id=uid(), name="Extra Day Off",        description="Redeem for 1 additional leave day",            cost=1000.0, stock=5,  status="active"),
            Reward(id=uid(), name="Eco Gift Hamper",      description="Sustainably sourced gift basket",              cost=500.0,  stock=10, status="active"),
            Reward(id=uid(), name="Plant a Tree",         description="A tree is planted in your name",               cost=100.0,  stock=50, status="active"),
            Reward(id=uid(), name="Charity Donation 25",  description="Donate to your chosen environmental charity",  cost=250.0,  stock=20, status="active"),
        ]
        db.add_all(rewards)

        # ── Notifications ────────────────────────────────────────────────────
        notifs = []
        for user_key in user_ids.values():
            notifs += [
                Notification(id=uid(), user_id=user_key, title="New Challenge Available!",        message="Zero-Waste Lunch Week challenge is now live. Join now to earn 150 points!", is_read=False, status="active"),
                Notification(id=uid(), user_id=user_key, title="Department Score Updated",        message="Your department ESG score increased by 3 points this month. Great work!",  is_read=False, status="active"),
                Notification(id=uid(), user_id=user_key, title="Compliance Reminder",             message="Q1 GHG inventory submission is due in 7 days. Please review your data.",    is_read=True,  status="active"),
                Notification(id=uid(), user_id=user_key, title="CSR Activity Approved ✅",       message="'Community Tree Planting Drive' has been approved. 300 points credited!",    is_read=True,  status="active"),
            ]
        db.add_all(notifs)

        await db.commit()
        print("✅ Seed complete! Inserted:")
        print(f"   • {len(departments)} departments")
        print(f"   • {len(users)} users")
        print(f"   • {len(categories)} categories")
        print(f"   • {len(efs)} emission factors")
        print(f"   • {len(txns)} carbon transactions (6-month trend)")
        print(f"   • {len(csr_activities)} CSR activities")
        print(f"   • {len(challenges)} challenges + {len(participations)} participations")
        print(f"   • {len(issues)} compliance issues")
        print(f"   • {len(scores)} department scores (6-month history)")
        print(f"   • {len(goals)} goals")
        print(f"   • {len(policies)} policies")
        print(f"   • {len(badges)} badges")
        print(f"   • {len(rewards)} rewards")
        print(f"   • {len(notifs)} notifications")
        print()
        print("🔑 Demo login credentials (any of these):")
        print("   alice@ecosphere.com  / password123  (admin)")
        print("   bob@ecosphere.com    / password123  (manager)")
        print("   carol@ecosphere.com  / password123  (employee)")


if __name__ == "__main__":
    asyncio.run(seed())
