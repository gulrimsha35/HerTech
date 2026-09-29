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

    if data_type == "id":
        return fake.uuid4()

    if data_type == "category":
        return random.choice(column.get("values", []))

    if data_type == "text":
        return fake.text()

    return fake.word()


def generate_dataset(schema):
    dataset = []

    for _ in range(schema["rows"]):
        record = {}

        for column in schema["columns"]:
            record[column["name"]] = generate_value(column)

        dataset.append(record)

    return dataset