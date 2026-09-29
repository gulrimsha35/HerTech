from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import GenerateRequest
from app.planner import create_schema, create_relational_schema
from app.generator import generate_dataset
from app.validator import validate_dataset
from app.exporter import export_csv, export_json
from app.planner import create_relational_schema
from app.relational_generator import generate_relational_data
from app.relational_validator import validate_relational_data
from app.exporter import export_relational_csv, export_relational_json, export_relational_sql
import json

app = FastAPI(title="HackData AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {
        "message": "HackData AI backend is ready."
    }


@app.post("/generate")
def generate_data(request: GenerateRequest):
    schema = create_schema(request.prompt)
    dataset = generate_dataset(schema)
    validation = validate_dataset(schema, dataset)

    return {
    "prompt": request.prompt,
    "schema": schema,
    "validation": validation,
    "data": dataset,
    "csv": export_csv(dataset),
    "json": export_json(dataset)
}
@app.post("/generate-relational")
def generate_relational(request: GenerateRequest):
    schema_text = create_relational_schema(request.prompt)

    schema = json.loads(schema_text)

    data = generate_relational_data(schema)

    validation = validate_relational_data(schema, data)

    csv_files = export_relational_csv(data)

    json_data = export_relational_json(data)

    sql_data = export_relational_sql(schema, data)

    return {
        "prompt": request.prompt,
        "schema": schema,
        "validation": validation,
        "data": data,
        "csv": csv_files,
        "json": json_data,
        "sql": sql_data
    }