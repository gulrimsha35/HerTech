import os
import json
from typing import List, Optional

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class ColumnPlan(BaseModel):
    name: str
    type: str
    min: Optional[int] = None
    max: Optional[int] = None
    values: Optional[List[str]] = None


class DatasetPlan(BaseModel):
    rowCount: int
    columns: List[ColumnPlan]


def create_schema(user_prompt):
    instructions = f"""
Convert the user's synthetic data request into a dataset schema.

User request:
{user_prompt}

Rules:
- Extract the number of rows.
- Extract every requested column.
- Use only these data types:
  name, email, phone, city, address, company, job, date,
  integer, float, boolean, id, category, text
- For integer ranges, use min and max.
- For float ranges, use min and max.
- For fields with a fixed set of choices, use category and values.
- For IDs, use type id.
- Do not generate any actual dataset rows.
- Return only the requested schema.
"""

    response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents=instructions,
    config={
        "response_mime_type": "application/json",
        "temperature": 0
    },
)
    data = json.loads(response.text)

    if isinstance(data, list):
        data = data[0]

    if "num_rows" in data:
        data["rowCount"] = data.pop("num_rows")

    schema = DatasetPlan.model_validate(data).model_dump()
    schema["rows"] = schema.pop("rowCount")

    for column in schema["columns"]:
        column["name"] = column["name"].strip().lower().replace(" ", "_")

    return schema

def create_relational_schema(user_prompt):
    instructions = f"""
Convert the user's relational synthetic data request into a database schema.

User request:
{user_prompt}

Return ONLY valid JSON.

The JSON must be an array of table objects.

Every table object MUST have exactly these fields:
- table
- rows
- columns

The "table" field must contain the table name.
The "rows" field must contain the number of records.

Every column object MUST have exactly these fields:
- name
- type
- description
- primary_key
- foreign_key

The "description" field must briefly explain what the column represents.
For example:
- course title -> "name of the academic course"
- product name -> "name of the product"
- patient age -> "age of the patient"

Use null for foreign_key when the column is not a foreign key.

For a foreign key, use this exact format:
"table_name.column_name"

Example:
"foreign_key": "students.student_id"

Allowed types:
name, email, phone, city, address, company, job, date,
integer, float, boolean, id, category, text

Rules:
- Identify every table requested by the user.
- Identify all requested columns.
- Identify the primary key of each table.
- Identify foreign-key relationships.
- Extract row counts from the user's request.
- Use the description to explain the semantic meaning of each column.
- Do not generate actual data rows.
- Do not add extra fields.
"""

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=instructions,
        config={
            "response_mime_type": "application/json"
        },
    )

    return response.text