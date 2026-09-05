"""Show that the shipped portal export emits a placeholder, unsigned receipt URL."""

from datetime import date, datetime
from decimal import Decimal

from travel_plan_permission.export import ExportService
from travel_plan_permission.models import ExpenseCategory, ExpenseItem, ExpenseReport


def main() -> None:
    report = ExpenseReport(
        report_id="report-1",
        trip_id="trip-1",
        traveler_name="Alice",
        expenses=[
            ExpenseItem(
                category=ExpenseCategory.LODGING,
                description="Hotel",
                amount=Decimal("250.00"),
                expense_date=date(2026, 9, 1),
                receipt_url="receipts/alice-hotel.pdf",
            )
        ],
    )
    _filename, csv_content = ExportService().to_csv(
        [report], batch_id="batch-1", now=datetime(2026, 9, 5)
    )

    assert "https://receipts.example.com/receipts/alice-hotel.pdf?expires_at=" in csv_content
    assert "signature=" not in csv_content
    print(csv_content)


if __name__ == "__main__":
    main()
