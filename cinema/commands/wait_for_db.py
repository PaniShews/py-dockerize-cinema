import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Waits for the database to be available."

    def add_arguments(self, parser):
        parser.add_argument(
            "--poll-interval",
            type=float,
            default=1.0,
            help="Seconds to wait between connection attempts (default: 1).",
        )

    def handle(self, *args, **options):
        interval = options["poll_interval"]
        self.stdout.write("Waiting for database...")

        db_conn = None
        while not db_conn:
            try:
                connections["default"].ensure_connection()
                db_conn = True
            except OperationalError:
                self.stdout.write(
                    f"Database unavailable, retrying in {interval}s..."
                )
                time.sleep(interval)

        self.stdout.write(self.style.SUCCESS("Database available!"))
