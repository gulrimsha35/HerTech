from faker import Faker
import random

fake = Faker()


def generate_value(column):
    data_type = column["type"]

    if data_type == "name":
        return fake.name()

    if data_type == "email":
        return fake.email()

    if data_type == "phone":
        return fake.phone_number()

    if data_type == "city":
        return fake.city()

    if data_type == "address":
        return fake.address()

    if data_type == "company":
        return fake.company()

    if data_type == "job":
        return fake.job()

    if data_type == "date":
        return str(fake.date())

    if data_type == "integer":
        minimum = column.get("min", 1)
        maximum = column.get("max", 100)
        return random.randint(minimum, maximum)

    if data_type == "float":
        minimum = column.get("min", 0)
        maximum = column.get("max", 1000)
        return round(random.uniform(minimum, maximum), 2)

    if data_type == "boolean":
        return random.choice([True, False])

    if data_type == "category":
        values = column.get("values", [])

        if values:
            return random.choice(values)

        return fake.word()

    if data_type == "text":
        description = column.get("description", "").lower()

        if "course" in description:
            return random.choice([
                "Database Systems",
                "Artificial Intelligence",
                "Data Structures",
                "Software Engineering",
                "Computer Networks",
                "Operating Systems",
                "Web Development",
                "Mobile Application Development"
            ])

        if "product" in description and "name" in description:
            return random.choice([
                "Wireless Mouse",
                "Laptop Stand",
                "USB Keyboard",
                "Bluetooth Speaker",
                "Webcam",
                "Power Bank"
            ])

        if "department" in description:
            return random.choice([
                "Computer Science",
                "Electrical Engineering",
                "Software Engineering",
                "Business Administration"
            ])

        return fake.sentence()

    if data_type == "id":
        return fake.uuid4()

    return fake.word()
def get_table_dependencies(table):
    dependencies = set()

    for column in table["columns"]:
        foreign_key = column.get("foreign_key")

        if foreign_key:
            referenced_table, _ = foreign_key.split(".")
            dependencies.add(referenced_table)

    return dependencies
def sort_tables_by_dependencies(schema):
    remaining = {table["table"]: table for table in schema}
    sorted_tables = []

    while remaining:
        added_table = False

        for table_name, table in list(remaining.items()):
            dependencies = get_table_dependencies(table)

            if dependencies.issubset(
                {table["table"] for table in sorted_tables}
            ):
                sorted_tables.append(table)
                del remaining[table_name]
                added_table = True

        if not added_table:
            raise ValueError("Circular or invalid table dependency detected.")

    return sorted_tables


def generate_relational_data(schema):
    sorted_schema = sort_tables_by_dependencies(schema)

    tables = {}

    for table in sorted_schema:
        table_name = table["table"]
        row_count = table["rows"]

        records = []

        for row_number in range(1, row_count + 1):
            record = {}

            for column in table["columns"]:
                column_name = column["name"]

                if column["primary_key"]:
                    record[column_name] = row_number
                    continue

                foreign_key = column.get("foreign_key")

                if foreign_key:
                    referenced_table, referenced_column = foreign_key.split(".")

                    referenced_records = tables[referenced_table]

                    record[column_name] = random.choice(
                        referenced_records
                    )[referenced_column]

                else:
                    record[column_name] = generate_value(column)

            records.append(record)

        tables[table_name] = records

    return tables