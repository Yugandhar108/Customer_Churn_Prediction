import csv
import random
from pathlib import Path


FIELDNAMES = [
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn",
]
DEMO_ROW_COUNT = 200
RANDOM_SEED = 42
SOURCE_SAMPLE_IDS = {
    "7590-VHVEG",
    "5575-GNVDE",
    "3668-QPYBK",
    "7795-CFOCW",
    "9237-HQITU",
}
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "customer_churn.csv"


def generate_demo_row(row_number, randomizer):
    churn = row_number % 2
    tenure = (
        1 + (row_number * 11) % 24
        if churn
        else 24 + (row_number * 7) % 49
    )
    internet_service = ["DSL", "Fiber optic", "DSL", "No", "Fiber optic"][
        row_number % 5
    ]
    service_base = {"DSL": 35.0, "Fiber optic": 65.0, "No": 20.0}[
        internet_service
    ]
    monthly_charges = round(service_base + randomizer.uniform(0, 45), 2)
    phone_service = randomizer.choices(["Yes", "No"], weights=[9, 1])[0]
    multiple_lines = (
        randomizer.choice(["Yes", "No"])
        if phone_service == "Yes"
        else "No phone service"
    )

    if internet_service == "No":
        internet_options = ["No internet service"] * 4
    else:
        internet_options = [randomizer.choice(["Yes", "No"]) for _ in range(4)]

    contract = randomizer.choices(
        ["Month-to-month", "One year", "Two year"],
        weights=[8, 1, 1] if churn else [5, 3, 2],
    )[0]

    return {
        "customerID": f"SYNTH-{row_number:06d}",
        "gender": randomizer.choice(["Female", "Male"]),
        "SeniorCitizen": randomizer.choices([0, 1], weights=[8, 2])[0],
        "Partner": randomizer.choice(["Yes", "No"]),
        "Dependents": randomizer.choice(["Yes", "No"]),
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": internet_options[0],
        "OnlineBackup": internet_options[1],
        "DeviceProtection": internet_options[2],
        "TechSupport": internet_options[3],
        "StreamingTV": randomizer.choice(["Yes", "No"])
        if internet_service != "No"
        else "No internet service",
        "StreamingMovies": randomizer.choice(["Yes", "No"])
        if internet_service != "No"
        else "No internet service",
        "Contract": contract,
        "PaperlessBilling": randomizer.choice(["Yes", "No"]),
        "PaymentMethod": randomizer.choice(
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
            ]
        ),
        "MonthlyCharges": f"{monthly_charges:.2f}",
        "TotalCharges": f"{monthly_charges * tenure:.2f}",
        "Churn": churn,
    }


def main():
    randomizer = random.Random(RANDOM_SEED)
    with CSV_PATH.open("r", newline="", encoding="utf-8-sig") as source_file:
        reader = csv.DictReader(source_file)
        if reader.fieldnames != FIELDNAMES:
            raise ValueError("The existing CSV header does not match the expected schema.")
        original_rows = [
            row for row in reader if not row["customerID"].startswith("SYNTH-")
        ]
    if {row["customerID"] for row in original_rows} != SOURCE_SAMPLE_IDS:
        raise ValueError(
            "This demo generator only accepts the original five screenshot rows. "
            "It will not append synthetic rows to a replacement/full dataset."
        )

    demo_rows = [
        generate_demo_row(row_number, randomizer)
        for row_number in range(1, DEMO_ROW_COUNT + 1)
    ]
    rows = original_rows + demo_rows

    with CSV_PATH.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    class_counts = {
        label: sum(int(row["Churn"]) == label for row in rows)
        for label in (0, 1)
    }
    print(f"Updated {CSV_PATH}")
    print(f"Total records: {len(rows)} (including {DEMO_ROW_COUNT} synthetic demo rows)")
    print(f"Churn label counts: {class_counts}")


if __name__ == "__main__":
    main()