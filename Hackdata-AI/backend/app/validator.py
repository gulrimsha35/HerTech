def validate_dataset(schema, dataset):
    errors = []

    if len(dataset) != schema["rows"]:
        errors.append(
            f"Expected {schema['rows']} rows but generated {len(dataset)}."
        )

    for row_number, record in enumerate(dataset, start=1):

        for column in schema["columns"]:
            column_name = column["name"]
            column_type = column["type"]

            if column_name not in record:
                errors.append(
                    f"Row {row_number}: missing column '{column_name}'."
                )
                continue

            value = record[column_name]

            if column_type == "integer":
                if not isinstance(value, int):
                    errors.append(
                        f"Row {row_number}: '{column_name}' must be an integer."
                    )
                else:
                    minimum = column.get("min")
                    maximum = column.get("max")

                    if minimum is not None and value < minimum:
                        errors.append(
                            f"Row {row_number}: '{column_name}' is below minimum."
                        )

                    if maximum is not None and value > maximum:
                        errors.append(
                            f"Row {row_number}: '{column_name}' is above maximum."
                        )

            if column_type == "float":
                if not isinstance(value, (int, float)):
                    errors.append(
                        f"Row {row_number}: '{column_name}' must be a number."
                    )

            if column_type == "category":
                allowed_values = column.get("values", [])

                if value not in allowed_values:
                    errors.append(
                        f"Row {row_number}: '{column_name}' has an invalid value."
                    )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }