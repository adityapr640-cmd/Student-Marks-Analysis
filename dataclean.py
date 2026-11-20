import numpy as np
import pandas as pd

# Read raw student marks CSV
raw_records = pd.read_csv('student.csv')
print("--- Raw Input Records (Top 10) ---")
print(raw_records.head(10))

# Deduplicate records based on Student_ID (keep primary student row)
raw_records = raw_records.drop_duplicates(subset=['Student_ID'], keep='first').copy()
print("\n--- Records After Deduplicating Student_ID ---")
print(raw_records.head(10))

# Normalize Gender column values into 'M' and 'F'
raw_records['Gender'] = raw_records['Gender'].astype(str).str.strip().str.upper()
gender_dict = {
    'FEMALE': 'F',
    'F': 'F',
    'MALE': 'M',
    'M': 'M'
}
raw_records['Gender'] = raw_records['Gender'].map(gender_dict).fillna('Unknown')
print("\n--- Records After Gender Normalization ---")
print(raw_records.head(10))

# Standardize Semester field to '1'
raw_records['Semester'] = raw_records['Semester'].astype(str).str.strip().str.upper()
semester_dict = {
    '4': '1',
    '3': '1',
    '2': '1',
    '1': '1'
}
raw_records['Semester'] = raw_records['Semester'].map(semester_dict).fillna('Unknown')

# Parse Student_ID suffix, order numerically, and reformat ID prefix
raw_records['Student_ID'] = raw_records['Student_ID'].str[5:]
raw_records['Student_ID'] = pd.to_numeric(raw_records['Student_ID'])
raw_records = raw_records.sort_values(by='Student_ID')
raw_records['Student_ID'] = '2026B0' + raw_records['Student_ID'].astype(str)

# Convert 'Absent' entries in Electrical_Marks to NaN
raw_records['Electrical_Marks'] = raw_records['Electrical_Marks'].astype(str).str.strip()
raw_records.loc[raw_records['Electrical_Marks'] == 'Absent', 'Electrical_Marks'] = np.nan

# Cast attendance and exam scores to numeric float dtype
score_and_att_cols = [
    'Attendance_Pct',
    'Maths_Marks',
    'Physics_Marks',
    'Programming_Marks',
    'Electrical_Marks',
    'AI_Marks'
]
for column in score_and_att_cols:
    raw_records[column] = pd.to_numeric(raw_records[column], errors='coerce')

# Enforce [0, 100] bounds on Attendance_Pct and fill out-of-range/missing with median
raw_records.loc[(raw_records['Attendance_Pct'] < 0) | (raw_records['Attendance_Pct'] > 100), 'Attendance_Pct'] = np.nan
raw_records['Attendance_Pct'] = raw_records['Attendance_Pct'].fillna(raw_records['Attendance_Pct'].median())

# Enforce [0, 100] bounds on all five subject mark columns and replace invalid/NaN with 0
exam_subjects = [
    'Maths_Marks',
    'Physics_Marks',
    'Programming_Marks',
    'Electrical_Marks',
    'AI_Marks'
]
for subject in exam_subjects:
    raw_records.loc[(raw_records[subject] < 0) | (raw_records[subject] > 100), subject] = np.nan
    raw_records[subject] = raw_records[subject].fillna(0)

print("\n--- Sanitized Output Records (Top 10) ---")
print(raw_records.head(10))

# Export cleaned records to CSV
raw_records.to_csv('cleaned_student.csv', index=False)
print("\nExport complete: cleaned_student.csv")