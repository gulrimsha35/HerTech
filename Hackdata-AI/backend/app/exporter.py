import csv
import json
import io


def export_csv(dataset):
    output = io.StringIO()

    if not dataset:
        return ""

    fieldnames = dataset[0].keys()

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(dataset)

    return output.getvalue()


def export_json(dataset):
    return json.dumps(dataset, indent=2)
def export_relational_csv(data):
    output = {}

    for table_name, records in data.items():
        output[table_name] = export_csv(records)

    return output
def export_relational_json(data):
    return json.dumps(data, indent=2)
def export_relational_sql(schema, data):
    sql = []

    for table in schema:
        table_name = table["table"]
        columns = table["columns"]

        column_definitions = []

        for column in columns:
            column_name = column["name"]
            column_type = column["type"]

            if column_type == "integer" or column_type == "id":
                sql_type = "INTEGER"
            elif column_type == "float":
                sql_type = "REAL"
            elif column_type == "boolean":
                sql_type = "BOOLEAN"
            else:
                sql_type = "TEXT"

            definition = f"{column_name} {sql_type}"

            if column["primary_key"]:
                definition += " PRIMARY KEY"

            foreign_key = column.get("foreign_key")

            if foreign_key:
                referenced_table, referenced_column = foreign_key.split(".")
                definition += (
                    f" REFERENCES {referenced_table}({referenced_column})"
                )

            column_definitions.append(definition)

        sql.append(
            f"CREATE TABLE {table_name} (\n"
            + ",\n".join(column_definitions)
            + "\n);"
        )

        for record in data[table_name]:
            values = []

            for column in columns:
                value = record[column["name"]]

                if isinstance(value, bool):
                    values.append("TRUE" if value else "FALSE")
                elif isinstance(value, (int, float)):
                    values.append(str(value))
                else:
                    value = str(value).replace("'", "''")
                    values.append(f"'{value}'")

            sql.append(
                f"INSERT INTO {table_name} "
                f"({', '.join(column['name'] for column in columns)}) "
                f"VALUES ({', '.join(values)});"
            )

    return "\n\n".join(sql)