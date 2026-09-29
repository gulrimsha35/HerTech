def validate_relational_data(schema, data):
    errors = []

    for table in schema:
        table_name = table["table"]
        records = data.get(table_name, [])

        if len(records) != table["rows"]:
            errors.append(
                f"{table_name}: expected {table['rows']} rows but found {len(records)}."
            )

        primary_keys = set()

        for record in records:
            for column in table["columns"]:

                column_name = column["name"]

                if column_name not in record:
                    errors.append(
                        f"{table_name}: missing column '{column_name}'."
                    )
                    continue

                if column["primary_key"]:
                    primary_key = record[column_name]

                    if primary_key in primary_keys:
                        errors.append(
                            f"{table_name}: duplicate primary key '{primary_key}'."
                        )

                    primary_keys.add(primary_key)

                foreign_key = column.get("foreign_key")

                if foreign_key:
                    referenced_table, referenced_column = foreign_key.split(".")

                    referenced_records = data.get(referenced_table, [])

                    referenced_values = {
                        row[referenced_column]
                        for row in referenced_records
                    }

                    if record[column_name] not in referenced_values:
                        errors.append(
                            f"{table_name}: foreign key '{column_name}' "
                            f"references a missing value."
                        )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }