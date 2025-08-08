import csv
import random
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

# ------------------- STEP 1: Generate Dataset -------------------

# Sample data pools
first_names = ["John", "Sarah", "Michael", "Emily", "Daniel", "Sophia", "David", "Olivia",
               "James", "Aisha", "Grace", "Emma", "Victor", "Amaka", "Ibrahim", "Chinedu",
               "Fatima", "Blessing", "Samuel", "Esther"]
last_names = ["Smith", "Johnson", "Brown", "Davis", "Wilson", "Miller", "Taylor", "Martin",
              "Anderson", "Okafor", "Olawale", "Adeyemi", "Ogunleye", "Okoro", "Abiola",
              "Ojo", "Eze", "Oluwaseun", "Nwachukwu", "Obi"]

genders = ["Male", "Female"]
diseases = ["Pneumonia", "Diabetes", "Fracture", "Malaria", "Covid-19",
            "Hypertension", "Asthma", "Tuberculosis", "Typhoid", "Cancer"]
doctors = ["Dr. Adams", "Dr. Lee", "Dr. Carter", "Dr. Patel", "Dr. Thompson",
           "Dr. Musa", "Dr. Ade", "Dr. Okeke", "Dr. Grace", "Dr. Bello"]

# Function to generate random date
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Create dataset
data = []
for i in range(1, 1501): # 1,500 patients (more than 1,000)
    patient_id = f"P{i:04}"
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    age = random.randint(1, 90)
    gender = random.choice(genders)
    disease = random.choice(diseases)
    doctor = random.choice(doctors)
    admission_date = random_date(datetime(2023, 1, 1), datetime(2025, 8, 1))
    discharge_date = admission_date + timedelta(days=random.randint(1, 21))
    bill_amount = round(random.uniform(500, 5000), 2)

    data.append([patient_id, name, age, gender, disease, doctor,
                 admission_date.strftime("%Y-%m-%d"),
                 discharge_date.strftime("%Y-%m-%d"),
                 bill_amount])

# Save to CSV
with open("hospital_database.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Patient_ID", "Name", "Age", "Gender", "Disease", "Doctor", 
        "Admission_Date", "Discharge_Date", "Bill_Amount"
    ])
    writer.writerows(data)

print("hospital_database.csv file with 1,500+ records created successfully!")

# ------------------- STEP 2: Load CSV into Pandas -------------------
df = pd.read_csv("hospital_database.csv")

# Convert dates to datetime
df['Admission_Date'] = pd.to_datetime(df['Admission_Date'])
df['Discharge_Date'] = pd.to_datetime(df['Discharge_Date'])

# ------------------- STEP 3: Create 9 Charts -------------------

# Chart 1: Gender Distribution
plt.figure(figsize=(6,4))
df['Gender'].value_counts().plot(kind='bar', color=['skyblue', 'pink'])
plt.title("Gender Distribution")
plt.ylabel("Number of Patients")
plt.xlabel("Gender")
plt.show()

# Chart 2: Top 10 Diseases
plt.figure(figsize=(8,5))
df['Disease'].value_counts().head(10).plot(kind='bar', color='orange')
plt.title("Top 10 Diseases")
plt.ylabel("Number of Cases")
plt.xlabel("Disease")
plt.show()

# Chart 3: Age Distribution Histogram
plt.figure(figsize=(8,5))
plt.hist(df['Age'], bins=20, color='green', edgecolor='black')
plt.title("Age Distribution of Patients")
plt.xlabel("Age")
plt.ylabel("Number of Patients")
plt.show()

# Chart 4: Average Bill Amount per Disease
plt.figure(figsize=(8,5))
df.groupby('Disease')['Bill_Amount'].mean().sort_values().plot(kind='barh', color='purple')
plt.title("Average Bill Amount by Disease")
plt.xlabel("Average Bill (₦)")
plt.ylabel("Disease")
plt.show()

# Chart 5: Patient Count by Doctor
plt.figure(figsize=(8,5))
df['Doctor'].value_counts().plot(kind='bar', color='teal')
plt.title("Patients per Doctor")
plt.ylabel("Number of Patients")
plt.xlabel("Doctor")
plt.show()

# Chart 6: Monthly Admissions Trend
monthly_admissions = df.groupby(df['Admission_Date'].dt.to_period('M')).size()
plt.figure(figsize=(10,5))
monthly_admissions.plot(kind='line', marker='o', color='blue')
plt.title("Monthly Admissions Trend")
plt.ylabel("Number of Admissions")
plt.xlabel("Month")
plt.show()

# Chart 7: Length of Stay Distribution
df['Length_of_Stay'] = (df['Discharge_Date'] - df['Admission_Date']).dt.days
plt.figure(figsize=(8,5))
plt.hist(df['Length_of_Stay'], bins=15, color='red', edgecolor='black')
plt.title("Length of Stay Distribution")
plt.xlabel("Days")
plt.ylabel("Number of Patients")
plt.show()

# Chart 8: Total Bill Amount per Month
monthly_bills = df.groupby(df['Admission_Date'].dt.to_period('M'))['Bill_Amount'].sum()
plt.figure(figsize=(10,5))
monthly_bills.plot(kind='bar', color='gold')
plt.title("Total Bill Amount Collected per Month")
plt.ylabel("Total Bill (₦)")
plt.xlabel("Month")
plt.show()

# Chart 9: Disease Proportion Pie Chart
plt.figure(figsize=(8,8))
df['Disease'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title("Proportion of Diseases")
plt.ylabel("")
plt.show()
