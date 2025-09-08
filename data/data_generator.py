import random
import pandas as pd
from faker import Faker
from datetime import timedelta

fake = Faker()

# ---------------- Config ----------------
NUM_PATIENTS = 10000
NUM_ENCOUNTERS = 24000  # total encounters
departments = ["Cardiology", "Oncology", "Orthopedics", "Respiratory", "General Medicine", "Surgery"]
encounter_types = ["A&E", "Outpatient", "Inpatient"]
hrg_codes = ["AA11A", "BB22B", "CC33C", "DD44D", "EB03Z", "FF55F"]

# ---------------- Patients ----------------
patients = []
for pid in range(1, NUM_PATIENTS + 1):
    patients.append({
        "PatientID": pid,
        "Name": fake.name(),
        "Age": random.randint(18, 90),
        "Gender": random.choice(["Male", "Female"]),
        "ChronicCondition": random.choice(["Diabetes", "Hypertension", "COPD", "Cancer", "None"]),
        "Postcode": fake.postcode()
    })
df_patients = pd.DataFrame(patients)

# ---------------- Encounters ----------------
encounters = []
admission_counter = 1

for eid in range(1, NUM_ENCOUNTERS + 1):
    patient = random.choice(patients)
    etype = random.choices(encounter_types, weights=[0.4, 0.4, 0.2])[0]
    encounter_date = fake.date_between(start_date="-1y", end_date="today")
    
    outcome = "Discharged"
    admission_id = None
    
    if etype == "Inpatient":
        outcome = random.choice(["Admitted", "Transferred", "Deceased"])
        admission_id = f"ADM{admission_counter:05d}"
        admission_counter += 1

    encounters.append({
        "EncounterID": f"ENC{eid:05d}",
        "PatientID": patient["PatientID"],
        "EncounterType": etype,
        "Department": random.choice(departments),
        "EncounterDate": encounter_date,
        "Outcome": outcome,
        "AdmissionID": admission_id
    })

df_encounters = pd.DataFrame(encounters)

# ---------------- Labs & Vitals ----------------
labs = []
for pid in range(1, NUM_PATIENTS + 1):
    labs.append({
        "PatientID": pid,
        "GlucoseLevel": random.randint(70, 250),
        "Cholesterol": random.randint(150, 300),
        "BloodPressure": f"{random.randint(100,160)}/{random.randint(60,100)}",
        "BMI": round(random.uniform(18, 40), 1)
    })
df_labs = pd.DataFrame(labs)

# ---------------- Hospital Costs (Inpatients) ----------------
hospital_costs = []
for pid in range(1, NUM_PATIENTS + 1):
    # Not all patients will have inpatient admissions
    if random.random() < 0.5:  # ~50% chance
        hospital_costs.append({
            "PatientID": pid,
            "HRGCode": random.choice(hrg_codes),
            "LengthOfStayDays": random.randint(1, 20),
            "CostPerStay": round(random.uniform(500, 15000), 2),
            "FundingType": random.choice(["NHS Funded", "Private", "Overseas Visitor"])
        })
df_hospital_costs = pd.DataFrame(hospital_costs)

# ---------------- Save CSVs ----------------
df_patients.to_csv("patients.csv", index=False)
df_encounters.to_csv("encounters.csv", index=False)
df_labs.to_csv("labs.csv", index=False)
df_hospital_costs.to_csv("hospital_costs.csv", index=False)

print("✅ Generated UK NHS-style datasets: patients.csv, encounters.csv, labs.csv, hospital_costs.csv")
