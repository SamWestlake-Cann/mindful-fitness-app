# test_bmi.py

from core.bmi_calculator import calculate_bmi

# Metric test
bmi, category = calculate_bmi(weight=70, height=1.75, unit="metric")
print(f"[Metric] BMI: {bmi}, Category: {category}")

# Imperial test
bmi, category = calculate_bmi(weight=154, height=69, unit="imperial")
print(f"[Imperial] BMI: {bmi}, Category: {category}")
