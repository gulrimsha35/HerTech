from app.planner import create_schema

print("Starting planner test...")

prompt = "Generate 10 students with name, age between 18 and 25, email and city."

print("Sending prompt to Google AI Studio...")

schema = create_schema(prompt)

print("Schema received!")
print(schema)