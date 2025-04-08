def calculate_bmi(weight, height, unit="metric"):

    if unit == "imperial":
        bmi = 703 * weight / (height ** 2)
    else:
        bmi = weight / (height ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Healthy"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return round(bmi, 2), category
