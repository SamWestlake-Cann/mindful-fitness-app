import customtkinter as ctk
import csv
from datetime import datetime
import re
import os

# Define path to BMI history inside "data" folder
BMI_HISTORY_FILE = "../data/bmi_history.csv"

# Initialise app window
app = ctk.CTk()
app.title("BMI Calculator")
app.geometry("500x700")
app.configure(bg="#000000")

# Set appearance to dark mode and apply a built-in theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Header Label for app
header = ctk.CTkLabel(app, text="BMI Calculator", font=(
    "Arial", 14), text_color="#f8b310",)
header.pack(pady=20)

# Name Input
name_label = ctk.CTkLabel(app, text="Enter your name:", font=(
    "Arial", 14), text_color="#f8b310",)
name_label.pack(pady=5)
name_entry = ctk.CTkEntry(app, width=250, height=40, font=(
    "Arial", 14), text_color="#f8b310",)
name_entry.pack(pady=10)

# Email Input
email_label = ctk.CTkLabel(app, text="Enter your email:", font=(
    "Arial", 14), text_color="#f8b310",)
email_label.pack(pady=5)
email_entry = ctk.CTkEntry(app, width=250, height=40, font=(
    "Arial", 14), text_color="#f8b310",)
email_entry.pack(pady=10)

# Consent Check box
consent_var = ctk.BooleanVar()
consent_checkbox = ctk.CTkCheckBox(app, text="I agree to save my BMI data",
                                   variable=consent_var, text_color="#f8b310",)
consent_checkbox.pack(pady=10)

# Height and weight input
height_label = ctk.CTkLabel(app, text="Enter your height (m):", font=(
    "Arial", 14), text_color="#f8b310",)
height_label.pack(pady=10)
height_entry = ctk.CTkEntry(app, width=250, height=40, font=(
    "Arial", 14), text_color="#f8b310",)
height_entry.pack(pady=10)

# Weight input label and entry field
weight_label = ctk.CTkLabel(app, text="Enter your weight (kg):", font=(
    "Arial", 14), text_color="#f8b310",)
weight_label.pack(pady=10)
weight_entry = ctk.CTkEntry(app, width=250, height=40, font=(
    "Arial", 14), text_color="#f8b310",)
weight_entry.pack(pady=10)

# Function to calculate BMI and display category


def calculate_bmi():
    try:
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        height = float(height_entry.get().strip())
        weight = float(weight_entry.get().strip())

        # Validate name and email address
        if not name or not email:
            result_label.configure(
                text="Please enter your name and email.", text_color="#f8b310")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            result_label.configure(
                text="Please enter a valid email address.", text_color="#f8b310")
            return

        # Validate height and weight
        if height <= 0 or weight <= 0:
            result_label.configure(
                text="Height and weight must be positive values.", text_color="#f8b310")
            return

        # Calculate bmi
        bmi = weight / (height ** 2)

        # Determine BMI category
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Healthy weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        # Display result to user
        result_label.configure(
            text=f"Your BMI is {bmi:.2f} ({category})\nHeight: {height} m\nWeight: {weight} kg", text_color=f"#f8b310")

        # Save BMI result to CSV if user consent
        if consent_var.get():
            save_bmi_result(name, email, height, weight, bmi, category)

    except ValueError:
        # If user enters non-numeric input
        result_label.configure(
            text="Please enter valid numbers.", text_color="#f8b310")


# Save BMI result to CSV file for logging
def save_bmi_result(name, email, height, weight, bmi, category):
    file_exists = os.path.isfile(BMI_HISTORY_FILE)
    with open(BMI_HISTORY_FILE, mode="a", newline="") as file:

        # Initialise writer
        writer = csv.writer(file)

        # Check if file exists is new or empty before writing header
        if not file_exists or os.stat(BMI_HISTORY_FILE).st_size == 0:
            writer.writerow(["Timestamp", "Name", "Email",
                            "Height (m)", "Weight (kg)", "BMI", "Category"])

        # Format the data for readability
        formatted_data = [
            datetime.now().strftime("Date: %Y-%m-%d, Time: %H:%M:%S "),
            f" Name: {name}",
            f" Email: {email}",
            f" Height: {height}",
            f" Weight: {weight}",
            f" BMI: {bmi:.2f}",
            f" Category: {category}"
        ]

        # Write the actual data
        writer.writerow(formatted_data)

# Reset all fields and result label


def reset_fields():
    name_entry.delete(0, ctk.END)
    email_entry.delete(0, ctk.END)
    height_entry.delete(0, ctk.END)
    weight_entry.delete(0, ctk.END)
    consent_var.set(False)
    result_label.configure(
        text="Your BMI will appear here", text_color="#f8b310")


# Calculate button
calculate_button = ctk.CTkButton(
    app, text="Calculate BMI", command=calculate_bmi, width=200, height=40, font=("Arial", 14, "bold"), fg_color="#f8b310", text_color="white")
calculate_button.pack(pady=20)

# Reset button to clear inputs and result
reset_button = ctk.CTkButton(app, text="Reset", command=reset_fields,
                             width=200, height=40, font=("Arial", 14, "bold"), fg_color="#f8b310", text_color="white")
reset_button.pack(pady=10)

# Result Label
result_label = ctk.CTkLabel(app, text="Your BMI will appear here", font=(
    "Arial", 18), text_color="#f8b310",)
result_label.pack(pady=10)

# Footer for app branding or contact information
footer = ctk.CTkLabel(app, text="Mindful Fitness App | Contact: info@mindfulsportscoach.co.uk",
                      font=("Arial", 12), text_color="#f8b310",)
footer.pack(side="bottom", pady=10)

# Run the app
app.mainloop()
