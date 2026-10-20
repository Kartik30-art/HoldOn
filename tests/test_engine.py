import unittest

from server.engine import assess_message, next_steps


class TestHoldOnEngine(unittest.TestCase):

    def test_otp_message_is_high_risk(self):
        result = assess_message("Share your OTP immediately.")
        self.assertEqual(result["risk_level"], "high")
        self.assertGreater(result["warning_count"], 0)

    def test_suspicious_link_is_detected(self):
        result = assess_message("Check this link: http://example.com")
        categories = [item["category"] for item in result["warning_signs"]]
        self.assertIn("contains_link", categories)

    def test_www_link_is_detected(self):
        result = assess_message("Visit www.example.com")
        categories = [item["category"] for item in result["warning_signs"]]
        self.assertIn("contains_link", categories)

    def test_link_alone_is_low_risk(self):
        result = assess_message("Visit http://example.com to read the article.")
        self.assertEqual(result["risk_level"], "low")

    def test_ordinary_message_is_low_risk(self):
        result = assess_message("Hello, are we meeting at 5 PM today?")
        self.assertEqual(result["risk_level"], "low")
        self.assertEqual(result["warning_count"], 0)

    def test_prize_and_payment_is_high_risk(self):
        result = assess_message(
            "You have won a prize. Pay processing fee immediately."
        )
        self.assertEqual(result["risk_level"], "high")

    def test_safety_advice_mentions_otp(self):
        result = assess_message("Share your OTP immediately.")
        steps = next_steps(result)
        self.assertTrue(any("OTP" in step for step in steps))

    def test_empty_message_is_rejected(self):
        for message in ("", "   "):
            with self.subTest(message=message):
                with self.assertRaises(ValueError):
                    assess_message(message)

    def test_required_fields_exist(self):
        result = assess_message("Hello there.")
        for field in ("risk_level", "warning_count", "warning_signs", "message"):
            self.assertIn(field, result)


if __name__ == "__main__":
    unittest.main()