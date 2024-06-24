from decimal import Decimal
import re

from services.usage.constans import VOWELS, BASE_COST


def find_words(text: str) -> str:
    """
       Extracts words from the input text using regular expressions.

       A word is defined as any continual sequence of letters (uppercase or lowercase),
       apostrophes ('), or hyphens (-).

       Args:
           text (str): The input text from which words will be extracted.

       Returns:
           str: A string containing all words found in the input text,
                separated by spaces.
       """
    words = re.findall(r"[a-zA-Z'-]+", text)
    result = ' '.join(words)
    return result


def find_word_lengths_cost(text: str) -> int:
    """
        Calculate the total cost based on the lengths of words in the input text.

        The cost is calculated as follows:
        - 0.1 for words with 3 or fewer characters.
        - 0.2 for words with 4 to 7 characters.
        - 0.3 for words with more than 7 characters.

        Args:
            text (str): The input text from which words will be extracted and evaluated.

        Returns:
            Decimal: The total cost based on the lengths of words in the text.
        """
    # Extract words from the text
    target_words = find_words(text)
    # Calculate the total cost based on word lengths
    total = sum(
        Decimal("0.1") if len(word) <= 3 else
        Decimal("0.2") if len(word) <= 7 else
        Decimal("0.3")
        for word in target_words.split()
    )
    return total


def find_character_count_cost(text: str) -> Decimal:
    """
        Calculate the cost based on the character count of the input text.

        The cost is calculated as:
        - 0.05 for each character in the text.

        Args:
            text (str): The input text for which the cost will be calculated.

        Returns:
            Decimal: The calculated cost based on the character count of the text.
        """
    return len(text) * Decimal("0.05")


def find_third_vowels_cost(text: str) -> int:
    """
    Calculate the total cost based on every third vowel in the input text.

    The cost is calculated as:
    - 0.3 for each vowel that is every third character starting from index 2.

    Args:
        text (str): The input text from which the cost will be calculated.

    Returns:
        Decimal: The calculated total cost based on every third vowel in the text.
    """
    total = sum(
        Decimal("0.3") for i in range(2, len(text), 3) if text[i].lower() in VOWELS
    )
    return total


def find_length_penalty(text: str) -> int:
    """
        Determine the penalty based on the length of the input text.

        The penalty is determined as:
        - 5 if the length of the text is greater than 100 characters.
        - 0 otherwise.

        Args:
            text (str): The input text for which the penalty will be determined.

        Returns:
            int: The calculated penalty based on the length of the text.
        """
    return 5 if len(text) > 100 else 0


def calculate_unique_word_bonus(text: str) -> int:
    """
    Calculates a bonus based on the uniqueness of words in the text.

    Args:
        text (str): The input text.

    Returns:
        int: A bonus of 2 if all words are unique, otherwise 0.
    """
    if not text:
        return 0

    target_words_split = find_words(text).split()
    are_unique = len(target_words_split) == len(set(target_words_split))
    return 2 if are_unique else 0


def is_palindrome(text: str) -> bool:
    """
    Checks if the given text is a palindrome. A palindrome is a string that reads
    the same forward and backward, ignoring non-alphanumeric characters and case.

    Args:
        text (str): The input text.

    Returns:
        bool: True if the text is a palindrome, False otherwise.
    """
    if not text:
        return False

    # Normalize the text: remove non-alphanumeric characters and convert to lowercase
    normalized_text = re.sub(r"[^a-zA-Z0-9]", "", text).lower()

    # Check if the normalized text is the same forward and backward
    return normalized_text == normalized_text[::-1]


def calculate_total_cost(text: str) -> float:
    """
    Calculate the total cost based on various criteria.

    Args:
        text (str): The input text.

    Returns:
        float: The calculated total cost.
    """
    character_count_cost = find_character_count_cost(text)
    word_lengths_cost = find_word_lengths_cost(text)
    third_vowels_cost = find_third_vowels_cost(text)
    length_penalty_cost = find_length_penalty(text)
    unique_word_bonus = calculate_unique_word_bonus(text)

    sub_total = (
        BASE_COST
        + character_count_cost
        + word_lengths_cost
        + third_vowels_cost
        + length_penalty_cost
        - unique_word_bonus
    )

    total = max(sub_total, BASE_COST)
    total *= 2 if is_palindrome(text) else 1

    return float(total)
