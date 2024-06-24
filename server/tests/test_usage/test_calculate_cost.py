import unittest
from decimal import Decimal
from services.usage.calculate_cost import (
    find_words,
    find_word_lengths_cost,
    find_character_count_cost,
    find_third_vowels_cost,
    find_length_penalty,
    calculate_unique_word_bonus,
    is_palindrome,
    calculate_total_cost
)
from services.usage.constans import BASE_COST


class TestCalculateCost(unittest.TestCase):

    def test_find_words(self):
        self.assertEqual(find_words("Hello, world!"), "Hello world")
        self.assertEqual(find_words("It's a test-case."), "It's a test-case")
        self.assertEqual(find_words(""), "")
        self.assertEqual(find_words("12345"), "")

    def test_find_word_lengths_cost(self):
        self.assertEqual(find_word_lengths_cost("a an ant"), Decimal("0.3"))
        self.assertEqual(find_word_lengths_cost("word longerword"), Decimal("0.5"))
        self.assertEqual(find_word_lengths_cost(""), Decimal("0"))

    def test_find_character_count_cost(self):
        self.assertEqual(find_character_count_cost("abc"), Decimal("0.15"))
        self.assertEqual(find_character_count_cost(""), Decimal("0"))
        self.assertEqual(find_character_count_cost("hello world"), Decimal("0.55"))

    def test_find_third_vowels_cost(self):
        self.assertEqual(find_third_vowels_cost("aebicoduf"), Decimal("0.3"))  # 'i' is the third character
        self.assertEqual(find_third_vowels_cost("aebicodufo"), Decimal("0.3"))  # 'i' is the only third vowel
        self.assertEqual(find_third_vowels_cost("aebicodufaei"), Decimal("0.6"))  # 'i' and 'i' are third vowels
        self.assertEqual(find_third_vowels_cost(""), Decimal("0"))
        self.assertEqual(find_third_vowels_cost("abcdefg"), Decimal("0"))

    def test_find_length_penalty(self):
        self.assertEqual(find_length_penalty("a" * 100), 0)
        self.assertEqual(find_length_penalty("a" * 101), 5)
        self.assertEqual(find_length_penalty(""), 0)

    def test_calculate_unique_word_bonus(self):
        self.assertEqual(calculate_unique_word_bonus("hello world"), 2)
        self.assertEqual(calculate_unique_word_bonus("hello hello"), 0)
        self.assertEqual(calculate_unique_word_bonus(""), 0)

    def test_is_palindrome(self):
        self.assertTrue(is_palindrome("A man a plan a canal Panama"))
        self.assertTrue(is_palindrome("racecar"))
        self.assertFalse(is_palindrome("hello"))
        self.assertFalse(is_palindrome(""))

    def test_calculate_total_cost(self):
        # Example calculations for better clarity
        text = "Hello world"
        character_count_cost = find_character_count_cost(text)  # 11 * 0.05 = 0.55
        word_lengths_cost = find_word_lengths_cost(text)  # Hello = 0.2, world = 0.2 -> total 0.4
        third_vowels_cost = find_third_vowels_cost(text)  # no third vowels -> 0
        length_penalty_cost = find_length_penalty(text)  # length = 11 -> 0
        unique_word_bonus = calculate_unique_word_bonus(text)  # unique words -> 2

        expected_total_cost = BASE_COST + character_count_cost + word_lengths_cost + third_vowels_cost + length_penalty_cost - unique_word_bonus
        expected_total_cost = float(max(expected_total_cost, BASE_COST))

        self.assertEqual(calculate_total_cost(text), expected_total_cost)

        text = "A man a plan a canal Panama"
        character_count_cost = find_character_count_cost(text)  # 27 * 0.05 = 1.35
        word_lengths_cost = find_word_lengths_cost(
            text)  # A = 0.1, man = 0.1, a = 0.1, plan = 0.2, a = 0.1, canal = 0.2, Panama = 0.2 -> total 1.0
        third_vowels_cost = find_third_vowels_cost(
            text)  # 0.3 (third vowel 'a' at index 2) + 0.3 (third vowel 'a' at index 5) = 0.6
        length_penalty_cost = find_length_penalty(text)  # length = 27 -> 0
        unique_word_bonus = calculate_unique_word_bonus(text)  # non-unique words -> 0

        expected_total_cost = BASE_COST + character_count_cost + word_lengths_cost + third_vowels_cost + length_penalty_cost - unique_word_bonus
        expected_total_cost = float(max(expected_total_cost, BASE_COST)) * 2  # It's a palindrome

        self.assertEqual(calculate_total_cost(text), expected_total_cost)

        text = "abc" * 35
        character_count_cost = find_character_count_cost(text)  # 105 * 0.05 = 5.25
        word_lengths_cost = find_word_lengths_cost(text)  # 'abc' repeated 35 times -> 35 * 0.1 = 3.5
        third_vowels_cost = find_third_vowels_cost(text)  # every third character in 'abcabcabc...' -> 0.3 * 35 = 10.5
        length_penalty_cost = find_length_penalty(text)  # length = 105 -> 5
        unique_word_bonus = calculate_unique_word_bonus(text)  # not unique -> 0

        expected_total_cost = BASE_COST + character_count_cost + word_lengths_cost + third_vowels_cost + length_penalty_cost - unique_word_bonus
        expected_total_cost = float(max(expected_total_cost, BASE_COST))

        self.assertEqual(calculate_total_cost(text), expected_total_cost)


if __name__ == "__main__":
    unittest.main()
