import random
import pandas as pd
from faker import Faker
import os

fake = Faker()

# ============================================================
# CONFIGURATION
# ============================================================

TOTAL_SAMPLES = 20000  # Enough data for training all 4 models

TEAMS = [
    "Technical Support",
    "Product Support",
    "Customer Service",
    "IT Support",
    "Billing and Payments",
    "Returns and Exchanges",
    "Service Outages and Maintenance",
    "Sales and Pre-Sales",
    "Human Resources",
    "General Inquiry",
]

LANGUAGES = ["en", "de"]

TYPES = ["Incident", "Request", "Problem", "Change"]

# ============================================================
# STRONG SUBJECTS PER TEAM
# ============================================================

TEAM_SUBJECTS = {
    "Technical Support": [
        "Authentication service failure",
        "API timeout for multiple users",
        "Database connection crash",
        "Software application freezing repeatedly",
    ],
    "Product Support": [
        "Feature not working as expected",
        "Dashboard metrics incorrect",
        "Problem with product configuration",
    ],
    "Customer Service": [
        "Delayed response from support",
        "Follow-up needed for previous request",
        "Issue with customer handling",
    ],
    "IT Support": [
        "VPN failing for remote employees",
        "Internal email system outage",
        "Cannot access internal tools",
    ],
    "Billing and Payments": [
        "Invoice total incorrect",
        "Payment not reflected in account",
        "Refund taking too long",
    ],
    "Returns and Exchanges": [
        "Return request pending",
        "Product arrived damaged",
        "Need replacement for defective item",
    ],
    "Service Outages and Maintenance": [
        "Production system down",
        "Performance degradation after patch update",
        "Unexpected downtime detected",
    ],
    "Sales and Pre-Sales": [
        "Enterprise pricing inquiry",
        "Need product demo",
        "Clarification on license terms",
    ],
    "Human Resources": [
        "Salary calculation issue",
        "Payroll mismatch",
        "Need employment verification",
    ],
    "General Inquiry": [
        "Question about your services",
        "Need information on partnership",
        "Clarification needed on privacy policy",
    ],
}

# ============================================================
# TOPICS PER TEAM
# ============================================================

TEAM_TOPICS = {
    "Technical Support": ["authentication failure", "api timeout", "database crash"],
    "Product Support": ["feature configuration", "dashboard issue", "analytics error"],
    "Customer Service": ["response delay", "ticket mishandling"],
    "IT Support": ["vpn issue", "email delivery failure", "network outage"],
    "Billing and Payments": ["invoice mismatch", "refund delay", "payment failure"],
    "Returns and Exchanges": ["damaged item", "rma delay"],
    "Service Outages and Maintenance": ["production outage", "performance drop"],
    "Sales and Pre-Sales": ["pricing clarification", "license query"],
    "Human Resources": ["payroll mismatch", "leave calculation error"],
    "General Inquiry": ["service overview", "policy clarification"],
}

# ============================================================
# EMAIL TEMPLATE COMPONENTS
# ============================================================

TRIGGERS = [
    "after the recent update",
    "after a system migration",
    "after maintenance activity",
    "after configuration change",
]

ATTEMPTS = [
    "clearing cache",
    "restarting the application",
    "reinstalling the software",
    "checking login credentials",
]

IMPACTS = [
    "production environment",
    "multiple users",
    "critical business workflows",
    "internal reporting systems",
]

BODY_TEMPLATES = {
    "en": (
        "Hello team, I am facing an issue related to {topic}. "
        "This problem started {trigger}. I have already tried {attempt}, but the issue still persists. "
        "Currently, this is impacting {impact}. Please assist as soon as possible. Regards, {customer}."
    ),
    "de": (
        "Hallo Team, ich habe ein Problem im Zusammenhang mit {topic}. "
        "Das Problem trat {trigger} auf. Ich habe bereits {attempt} versucht, aber das Problem besteht weiterhin. "
        "Derzeit betrifft dies {impact}. Bitte um schnelle Unterstützung. Mit freundlichen Grüßen, {customer}."
    ),
}

ANSWER_TEMPLATES = {
    "en": (
        "Thank you for contacting us. Our {team} team is reviewing your issue regarding {topic}. "
        "Please try the following step: {action}. We will get back to you shortly if additional action is required."
    ),
    "de": (
        "Vielen Dank für Ihre Nachricht. Unser {team}-Team prüft Ihr Problem zu {topic}. "
        "Bitte versuchen Sie diesen Schritt: {action}. Wir melden uns bei weiteren Schritten."
    ),
}

# ============================================================
# ACTION MAPPINGS
# ============================================================

ACTION_MAP = {
    "Technical Support": ["restart_service", "check_config", "escalate_to_engineering"],
    "Service Outages and Maintenance": ["restart_service", "rollback_update", "notify_devops"],
    "Billing and Payments": ["review_invoice", "initiate_refund", "escalate_finance"],
    "Returns and Exchanges": ["approve_return", "issue_rma", "contact_logistics"],
    "IT Support": ["reset_vpn", "check_network", "restart_email_service"],
    "Product Support": ["reconfigure_feature", "provide_walkthrough", "create_bug_report"],
    "Customer Service": ["follow_up", "send_apology", "update_customer"],
    "Human Resources": ["adjust_payroll", "verify_records", "contact_hr_manager"],
    "Sales and Pre-Sales": ["send_pricing", "schedule_demo", "assign_account_manager"],
    "General Inquiry": ["send_information", "redirect_department", "close_ticket"],
}

# ============================================================
# PRIORITY RULES (STRONG SIGNAL)
# ============================================================

def get_priority(team, topic):
    topic = topic.lower()

    if any(w in topic for w in ["outage", "failure", "crash", "timeout"]):
        return "high"

    if any(w in topic for w in ["invoice", "refund", "payment", "rma"]):
        return "medium"

    if team == "General Inquiry":
        return "low"

    return random.choices(["low", "medium", "high"], weights=[0.2, 0.6, 0.2])[0]


# ============================================================
# TTR (Time-to-Resolve) RULES
# ============================================================

def get_ttr(priority):
    if priority == "high":
        return round(random.uniform(1, 4), 2)
    if priority == "medium":
        return round(random.uniform(4, 24), 2)
    return round(random.uniform(24, 72), 2)


# ============================================================
# GENERATE A SINGLE TICKET
# ============================================================

def generate_ticket(team):
    lang = random.choice(LANGUAGES)
    customer = fake.name()

    subject = random.choice(TEAM_SUBJECTS[team])
    topic = random.choice(TEAM_TOPICS[team])
    trigger = random.choice(TRIGGERS)
    attempt = random.choice(ATTEMPTS)
    impact = random.choice(IMPACTS)

    body = BODY_TEMPLATES[lang].format(
        topic=topic, trigger=trigger, attempt=attempt,
        impact=impact, customer=customer
    )

    action = random.choice(ACTION_MAP[team])
    answer = ANSWER_TEMPLATES[lang].format(team=team, topic=topic, action=action)

    priority = get_priority(team, topic)
    ttr = get_ttr(priority)

    return {
        "subject": subject,
        "body": body,
        "answer": answer,
        "type": random.choice(TYPES),
        "queue": team,
        "priority": priority,
        "language": lang,
        "tag_1": topic,
        "action": action,
        "ttr_hours": ttr,
    }


# ============================================================
# GENERATE FULL DATASET
# ============================================================

def generate_dataset():
    rows = []
    per_team = TOTAL_SAMPLES // len(TEAMS)

    for team in TEAMS:
        for _ in range(per_team):
            rows.append(generate_ticket(team))

    return pd.DataFrame(rows)


# ============================================================
# RUN SCRIPT
# ============================================================

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    df = generate_dataset()
    df.to_csv("data/raw/synthetic_tickets.csv", index=False)
    print(f"Generated {TOTAL_SAMPLES} high-quality rows → data/raw/synthetic_tickets.csv")














