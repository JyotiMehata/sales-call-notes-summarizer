# import csv
# import os


# def save_crm_record(crm_record):
#     """
#     Save the CRM record to a CSV file.
#     """

#     file_name = "crm_records.csv"

#     file_exists = os.path.exists(file_name)

#     with open(
#         file_name,
#         mode="a",
#         newline="",
#         encoding="utf-8"
#     ) as file:

#         writer = csv.DictWriter(
#             file,
#             fieldnames=[
#                 "Customer Name",
#                 "Summary",
#                 "Key Points",
#                 "Action Items",
#                 "Next Action",
#                 "CRM Status"
#             ]
#         )

#         # Create the header only when the file is new
#         if not file_exists:
#             writer.writeheader()

#         writer.writerow({
#             "Customer Name": crm_record["Customer Name"],
#             "Summary": crm_record["Summary"],
#             "Key Points": ", ".join(crm_record["Key Points"]),
#             "Action Items": ", ".join(crm_record["Action Items"]),
#             "Next Action": crm_record["Next Action"],
#             "CRM Status": crm_record["CRM Status"]
#         })




import csv
import os
from datetime import datetime


CSV_FILE = "crm_records.csv"

CSV_COLUMNS = [
    "Date and Time",
    "Customer Name",
    "Original Call Notes",
    "Cleaned Notes",
    "Summary",
    "Key Points",
    "Action Items",
    "Next Action",
    "CRM Status",
]


def save_crm_record(crm_record):
    """
    Save all input and generated CRM information to CSV.
    """

    file_exists = (
        os.path.exists(CSV_FILE)
        and os.path.getsize(CSV_FILE) > 0
    )

    # Add date and time if it was not supplied
    if not crm_record.get("Date and Time"):
        crm_record["Date and Time"] = (
            datetime.now().astimezone().isoformat(
                timespec="seconds"
            )
        )

    # Convert lists into readable text for CSV
    for field in ["Key Points", "Action Items"]:
        value = crm_record.get(field, [])

        if isinstance(value, list):
            crm_record[field] = " | ".join(value)

    with open(
        CSV_FILE,
        mode="a",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=CSV_COLUMNS,
            extrasaction="ignore"
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            column: crm_record.get(column, "")
            for column in CSV_COLUMNS
        })
