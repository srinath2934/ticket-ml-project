import random
import pandas as pd
from faker import Faker
import os

fake = Faker()

# ==============================================================
# CONFIG
# ==============================================================

TOTAL_SAMPLES = 200_000      # can increase as needed
LANGUAGES = ["en"]
PRIORITIES = ["low", "medium", "high"]

TEAMS = [
    "Technical Support", "Product Support", "Customer Service", "IT Support",
    "Billing and Payments", "Returns and Exchanges",
    "Service Outages and Maintenance", "Sales and Pre-Sales",
    "Human Resources", "General Inquiry",
]

TYPES = ["Incident", "Request", "Problem", "Change"]

# ==============================================================
# TYPE-SPECIFIC VOCABULARY (Strong signal separation)
# ==============================================================

TYPE_KEYWORDS = {
    "Incident": [
        "system outage", "critical failure", "service down", "urgent disruption",
        "complete outage", "major outage", "system stopped", "crash"
    ],
    "Request": [
        "requesting access", "need clarification", "asking for approval",
        "request information", "seeking support", "require help"
    ],
    "Problem": [
        "recurring issue", "persistent failure", "root cause necessary",
        "keeps happening", "underlying fault", "diagnostic required"
    ],
    "Change": [
        "change request", "deploy update", "configuration change",
        "apply migration", "schedule deployment", "environment update"
    ],
}

# ==============================================================
# TEAM-SPECIFIC SUBJECTS
# ==============================================================

TEAM_SUBJECTS = {
    "Technical Support": [
        "API timeout error", "System crash", "Authentication failure"
    ],
    "Product Support": [
        "Feature configuration issue", "Product settings confusion"
    ],
    "Customer Service": [
        "Support response delay", "Unresolved previous ticket"
    ],
    "IT Support": [
        "VPN not connecting", "Email delivery failure"
    ],
    "Billing and Payments": [
        "Incorrect billing amount", "Refund not processed"
    ],
    "Returns and Exchanges": [
        "Return request pending", "Damaged item received"
    ],
    "Service Outages and Maintenance": [
        "Production outage", "Performance degradation"
    ],
    "Sales and Pre-Sales": [
        "Enterprise pricing inquiry", "Need detailed quotation"
    ],
    "Human Resources": [
        "Payroll mismatch", "Leave balance incorrect"
    ],
    "General Inquiry": [
        "General question", "Need information on company policy"
    ]
}

# ==============================================================
# ACTION MAPPING BASED ON TYPE
# ==============================================================

ACTION_MAP = {
    "Incident": [
        "restart affected service",
        "trigger incident protocol",
        "notify engineering team"
    ],
    "Request": [
        "provide requested details",
        "verify user access",
        "approve access request"
    ],
    "Problem": [
        "perform root-cause analysis",
        "check logs for recurring patterns",
        "apply diagnostic steps"
    ],
    "Change": [
        "review configuration update",
        "schedule deployment window",
        "validate change request"
    ]
}

# ==============================================================
# REALISTIC TTR DISTRIBUTION (HOURS)
# ==============================================================

def generate_ttr(ticket_type, priority):
    base_ranges = {
        "Incident": (1, 6),
        "Problem": (10, 70),
        "Request": (8, 40),
        "Change": (3, 30),
    }

    low, high = base_ranges[ticket_type]

    if priority == "high":
        return random.uniform(low, low + (high - low) * 0.30)
    elif priority == "medium":
        return random.uniform(low + 1.5, high - 3)
    else:
        return random.uniform(low + 3, high)

# ==============================================================
# TONE STYLES FOR REALISM
# ==============================================================

TONES = {
    "formal": "I kindly request your assistance regarding this matter.",
    "angry": "This issue is unacceptable and needs immediate attention.",
    "confused": "I'm not sure why this is happening and would appreciate clarification.",
    "short": "Please resolve this soon.",
}

# ==============================================================
# GENERATE A SINGLE TICKET (FINAL LOGIC)
# ==============================================================

def generate_ticket(team):
    ticket_type = random.choice(TYPES)
    priority = random.choice(PRIORITIES)
    tone = random.choice(list(TONES.keys()))

    subject = random.choice(TEAM_SUBJECTS[team])
    keyword = random.choice(TYPE_KEYWORDS[ticket_type])
    customer = fake.name()

    # BODY GENERATION
    body = (
        f"Hello team, I'm reporting a {ticket_type.lower()} involving {keyword}. "
        f"{TONES[tone]} This started after a recent update. "
        f"I have already attempted initial troubleshooting. Regards, {customer}."
    )

    # ANSWER GENERATION
    answer = (
        f"Our {team} team has reviewed your {ticket_type.lower()}. "
        f"Recommended next step: {random.choice(ACTION_MAP[ticket_type])}. "
        f"We will update you shortly."
    )

    # TTR
    ttr = round(generate_ttr(ticket_type, priority), 2)

    return {
        "subject": subject,
        "body": body,
        "answer": answer,
        "type": ticket_type,
        "queue": team,
        "priority": priority,
        "language": "en",
        "tag_1": keyword,
        "action": random.choice(ACTION_MAP[ticket_type]),
        "ttr_hours": ttr,
        "full_text": subject + " " + body,
        "clean_text": (subject + " " + body).lower(),
    }

# ==============================================================
# GENERATE FULL DATASET
# ==============================================================

def generate_dataset():
    rows = []
    per_team = TOTAL_SAMPLES // len(TEAMS)

    for team in TEAMS:
        for _ in range(per_team):
            rows.append(generate_ticket(team))

    return pd.DataFrame(rows)

# ==============================================================
# MAIN
# ==============================================================

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)

    df = generate_dataset()
    df.to_csv("data/raw/ultra_synthetic_200k.csv", index=False)

    print(f"Generated ULTRA dataset with {TOTAL_SAMPLES} rows → data/raw/ultra_synthetic_200k.csv")
