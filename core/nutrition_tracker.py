import csv
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt


# Class wrapper
class NutritionTracker:
    def __init__(self, weekly_file="data/meal_history_week.csv"):
        self.weekly_file = weekly_file

    # save meal and calorie data to csv file:
    def save_meal_result(self, name, meal_name, calories, protein, carbs, fats, saturates, sugars, fibre):
        try:
            file_exists = os.path.isfile(self.weekly_file)
            with open(self.weekly_file, mode="a", newline="") as file:
                writer = csv.writer(file)

                # Write Header if the file is empty
                if not file_exists or os.stat(self.weekly_file).st_size == 0:
                    writer.writerow(["Timestamp", "Name", "Meal", "Calories",
                                    "Protein", "Carbs", "Fats", "Saturates", "Sugars", "Fibre"])
                writer.writerow([datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"), name, meal_name, calories, protein, carbs, fats, saturates, sugars, fibre])

        except Exception as e:
            print(f"Error saving meal result: {e}")

    # log meal

    def log_meal(self, name, meal_name, calories, protein, carbs, fats, saturates, sugars, fibre):
        missing_fields = []
        if not name:
            missing_fields.append("Name")
        if not meal_name:
            missing_fields.append("Meal Name")
        if not calories:
            missing_fields.append("Calories")
        if not protein:
            missing_fields.append("Protein")
        if not carbs:
            missing_fields.append("Carbs")
        if not fats:
            missing_fields.append("Fats")

        if missing_fields:
            return f"Please enter all meal details: {", ".join(missing_fields)}"

        try:
            # Check if the entries are positive digits
            try:
                calories = float(calories)
            except ValueError:
                return "Please enter a valid number for calories."

            try:
                calories = float(protein)
            except ValueError:
                return "Please enter a valid number for protein."

            try:
                calories = float(carbs)
            except ValueError:
                return "Please enter a valid number for carbs."

            try:
                calories = float(fats)
            except ValueError:
                return "Please enter a valid number for fats."

            if calories <= 0 or protein <= 0 or carbs <= 0 or fats <= 0:
                return "Values must be positive numbers."

            # Field Validation
            for label, value in [("Saturates", saturates), ("Sugars", sugars), ("Fibre", fibre)]:
                if value and not value.replace(".", "", 1).isdigit():
                    return f"Please enter a valid number for {label}."

            # Convert to float
            saturates = float(saturates) if saturates.replace(
                ".", "", 1).isdigit() else 0
            sugars = float(sugars) if sugars.replace(
                ".", "", 1).isdigit() else 0
            fibre = float(fibre) if fibre.replace(".", "", 1).isdigit() else 0

            # Save meal result
            self.save_meal_result(name, meal_name, calories, protein,
                                  carbs, fats, saturates, sugars, fibre)
            return "Meal logged successfully"
        except ValueError:
            return "Please enter valid numbers for all fields."
        except Exception as e:
            return f"Error: {e}"

    # Function to display pie chart for meal macros

    def display_meal_pie_chart(self, protein, carbs, fats, show=True):
        try:
            # Check for all-zero input
            if protein + carbs + fats <= 0:
                print("Cannot display pie chart: all values are zero or negative.")
                return False

            labels = ["Protein", "Carbs", "Fats"]
            sizes = [protein, carbs, fats]
            colors = ["#ff9999", "#66b3ff", "#99ff99"]

            plt.figure(figsize=(5, 5))
            plt.pie(sizes, labels=labels, colors=colors,
                    autopct="%1.1f%%", startangle=90)
            plt.title("Meal Macronutrient Breakdown")
            plt.axis("equal")  # equal aspect ensures pie drawn in a circle
            if show:
                plt.show()
            return True
        except Exception as e:
            print(f"Error displaying pie chart: {e}")
            return False

    def already_logged_today(self):
        if not os.path.exists(self.weekly_file):
            return False
        with open(self.weekly_file, "r") as file:
            for row in csv.reader(file):
                if row and row[0].startswith(datetime.now().strftime("%Y-%m-%d")):
                    return True
        return False

    # Function to display weekly summary as a bar chart

    def display_weekly_summary_chart(self, weekly_data):
        try:
            labels = list(weekly_data.keys())
            values = list(weekly_data.values())
            colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]

            plt.figure(figsize=(8, 5))
            plt.bar(labels, values, color=colors)
            plt.title("Weekly Nutritional Summary")
            plt.ylabel("Total Grams / Calories")
            plt.tight_layout()
            plt.show()
            return True
        except Exception as e:
            print(f"Error displaying weekly summary chart: {e}")
            return False

    # Utility function to check if the file is empty

    def is_file_empty(self, filepath):
        if not os.path.exists(filepath):
            return True
        return os.stat(filepath).st_size == 0

    # Function to generate weekly summary (save total calorie/macros)

    def generate_weekly_summary(self):
        weekly_data = {
            "Calories": 0,
            "Protein": 0,
            "Carbs": 0,
            "Fats": 0,
            "Sugars": 0,
            "Fibre": 0
        }

        try:
            seven_days_ago = datetime.now() - timedelta(days=7)

            # Read data from meal history CSV and aggregate for the week
            if os.path.isfile(self.weekly_file):
                with open(self.weekly_file, mode="r") as file:
                    reader = csv.reader(file)
                    next(reader)  # skip header row

                    for row in reader:
                        # Safe guard against malformed lines
                        if len(row) < 11:
                            continue

                        # Only include data from past 7 days
                        try:
                            row_date = datetime.strptime(
                                row[0], "%Y-%m-%d %H:%M:%S")
                            if row_date < seven_days_ago:
                                continue
                        except Exception:
                            continue  # Skip rows with invalid dates

                        weekly_data["Calories"] += int(row[3])
                        weekly_data["Protein"] += int(row[4])
                        weekly_data["Carbs"] += int(row[5])
                        weekly_data["Fats"] += int(row[6])
                        weekly_data["Sugars"] += int(row[9])
                        weekly_data["Fibre"] += int(row[10])

            # Save data to new CSV for the week totals and prevent duplicate
            if not self.already_logged_today():
                with open(self.weekly_file, mode="a", newline="") as file:
                    writer = csv.writer(file)

                    # Add header if the file is new/empty
                    file_empty = self.is_file_empty(self.weekly_file)
                    if file_empty:
                        writer.writerow(
                            ["Date", "Calories", "Protein", "Carbs", "Fats", "Sugars", "Fibre"])

                    writer.writerow([
                        datetime.now().strftime("%Y-%m-%d"),
                        weekly_data["Calories"],
                        weekly_data["Protein"],
                        weekly_data["Carbs"],
                        weekly_data["Fats"],
                        weekly_data["Sugars"],
                        weekly_data["Fibre"]
                    ])

                # Show visual summary
            self.display_weekly_summary_chart(weekly_data)
            return weekly_data

        except Exception as e:
            print(f'Error generating weekly summary: {e}')
            return None
