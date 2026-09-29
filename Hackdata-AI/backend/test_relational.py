from app.planner import create_relational_schema
from app.relational_generator import generate_relational_data
from app.relational_validator import validate_relational_data
from app.exporter import export_relational_csv
from app.exporter import export_relational_json
from app.exporter import export_relational_sql
import json

print("Starting relational generator test...")

prompt = """
Generate 10 students, 5 courses and 20 enrollments.

Students have student ID and name.
Courses have course ID and title.
Enrollments should connect students with courses.
"""

print("Creating relational schema...")

schema_text = create_relational_schema(prompt)

schema = json.loads(schema_text)

print("AI schema:")
print(json.dumps(schema, indent=2))

print("Generating relational data...")

data = generate_relational_data(schema)
sql_data = export_relational_sql(schema, data)

print("SQL export:")
print(sql_data[:3000])
csv_files = export_relational_csv(data)
json_data = export_relational_json(data)

print("JSON export:")
print(json_data[:1000])

print("CSV export:")

for table_name, csv_data in csv_files.items():
    print(f"\n--- {table_name}.csv ---")
    print(csv_data[:500])
validation = validate_relational_data(schema, data)

print("Validation:")
print(json.dumps(validation, indent=2))
print("Relational data generated!")

for table_name, records in data.items():
    print(table_name, ":", len(records), "rows")

print("Student IDs:", [row["student_id"] for row in data["students"]])

print("Enrollment student IDs:",
      [row["student_id"] for row in data["enrollments"][:5]])

print("Enrollment course IDs:",
      [row["course_id"] for row in data["enrollments"][:5]])