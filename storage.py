import csv
import os


def save_crm_record(crm_record):
    """
    Save the CRM record to a CSV file.
    """

    file_name = "crm_records.csv"

    file_exists = os.path.exists(file_name)

    with open(
        file_name,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Customer Name",
                "Summary",
                "Key Points",
                "Action Items",
                "Next Action",
                "CRM Status"
            ]
        )

        # Create the header only when the file is new
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "Customer Name": crm_record["Customer Name"],
            "Summary": crm_record["Summary"],
            "Key Points": ", ".join(crm_record["Key Points"]),
            "Action Items": ", ".join(crm_record["Action Items"]),
            "Next Action": crm_record["Next Action"],
            "CRM Status": crm_record["CRM Status"]
        })



