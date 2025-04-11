import unittest
from datetime import datetime
# Make sure this is the correct import path for your file
from core.nutrition_tracker import NutritionTracker


class TestNutritionTracker(unittest.TestCase):

    def setUp(self):
        """Set up a fresh instance of NutritionTracker before each test"""
        self.tracker = NutritionTracker(
            # This will create an instance of the NutritionTracker class
            "data/meal_history_week.csv")

    def test_log_meal_invalid_data(self):
        """Test logging a meal with invalid data"""
        result = self.tracker.log_meal(
            "", "Pasta", "not_a_number", 30, 20, 15, 5, 8, 4)
        self.assertEqual(result, "Please enter a valid number for calories.")

    def test_is_file_empty(self):
        """Test if the file is empty"""
        result = self.tracker.is_file_empty(
            self.tracker.weekly_file)  # Adjust the file path as needed
        # Check that the result is True if the file is empty
        self.assertTrue(result)

    def test_generate_weekly_summary(self):
        """Test generating the weekly summary"""
        weekly_summary = self.tracker.generate_weekly_summary()
        # Ensure the result is a dictionary
        self.assertIsInstance(weekly_summary, dict)
