def handle_doc_checker(data):
    """
    Check which fields are completed and identify if financial docs are submitted.
    """
    missing_fields = []
    has_financials = False

    fields_to_check = {
        "Bank Statement": "Bank_Statement",
        "PnL Statement": "PnL_Statement",
        "VAT Returns": "VAT_Returns",
        "ID Document": "ID_Document",
        "Business License": "Business_License"
    }

    for label, key in fields_to_check.items():
        value = data.get(key)
        if not value:
            missing_fields.append(label)
        if key in ["Bank_Statement", "PnL_Statement", "VAT_Returns"] and value:
            has_financials = True

    return {
        "missing_fields": missing_fields,
        "has_financials": has_financials
    }
