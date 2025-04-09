import customtkinter as ctk

# Initilise the app window
app = ctk.CTk()
app.title("BMI Calculator")
app.geometry("400x400")
app.config(bg="#000000")

# Set custom colours
ctk.set_appearance_mode("dark")  # Optional switch between dark/light mode
ctk.set_default_color_theme("f8b310")  # Using business colour yellow

# Header Label
header = ctk.CTkLabel(app, text="BMI Calculator", font=(
    "Arial", 24, "bold"), text_color="#f8b310", bg_color="#000000")
header.pack(pady=20)

# Height input
height_label = ctk.CTkLabel(app, text="Enter your height (m):", font=(
    "Arial", 14), text_color="#f8b310", bg_color="#000000")
height_label.pack(pady=10)
height_entry = ctk.CTkEntry(app, width=250, height=40, font=(
    "Arial", 14), text_color="#f8b310", bg_color="#000000")
height_entry.pack(pady=5)

# Weight input
weight_label = ctk.CTkLabel(app, text="Enter your weight (kg):", font=(
    "Arial", 14), text_color="#f8b310", bg_color="#000000")
weight_label.pack(pady=10)
weight_entry = ctk.CTkEntry(app, width=250, height=40, font=(
    "Arial", 14), text_color="f8b310", bg_color="#000000")
weight_entry.pack(pady=5)

# Function to calculate BMI


def calculate_bmi():
    try:
        height = float(height_entry.get())
        weight = float(weight_entry.get())
        bmi = weight / (height ** 2)
        result_label.config(text=f"Your BMI: {bmi:.2f}", text_color="f8b310")
    except ValueError:
        result_label.config(
            text="Please enter valid numbers.", text_color="f8b310")


# Calculate button
calculate_button = ctk.CTkButton(
    app, text="Calculate BMI", command=calculate_bmi, width=200, height=40, font=("Arial", 14, "bold"))
calculate_button.pack(pady=20)

# Result label
result_label = ctk.CTkLabel(app, text="Your BMI will appear here", font=(
    "Arial", 18), text_color="#f8b310", bg_color="#000000")
result_label.pack(pady=10)

# Run the app
app.mainloop()
