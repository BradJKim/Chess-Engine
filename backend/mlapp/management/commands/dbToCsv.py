import sqlite3
import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Export the first 20 items from SQLite database to CSV'

    def handle(self, *args, **kwargs):
        db_file = os.path.join(settings.BASE_DIR, 'test.db')  # Adjust this path as necessary
        table_name = 'evaluations'
        csv_file = os.path.join(settings.BASE_DIR, 'evals.csv')

        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()

            # Modify the SQL query to limit results to the first 20 items
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 10000")
            rows = cursor.fetchall()

            # Get column names
            column_names = [description[0] for description in cursor.description]

            with open(csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(column_names)  # Write column names
                writer.writerows(rows)          # Write first 20 rows

            self.stdout.write(self.style.SUCCESS('Data exported successfully to evals.csv!'))

        except sqlite3.Error as e:
            self.stderr.write(self.style.ERROR(f'SQLite error: {str(e)}'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))

        finally:
            if conn:
                conn.close()
