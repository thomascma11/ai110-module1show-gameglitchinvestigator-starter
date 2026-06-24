"""Pure game logic helpers for the Game Glitch Investigator project.

These functions intentionally avoid Streamlit so they can be tested with pytest.
"""


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive number range for a selected difficulty level."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 50),
    }
    return ranges.get(difficulty, ranges["Normal"])


def get_attempt_limit(difficulty: str) -> int:
    """Return the number of attempts allowed for the selected difficulty."""
    limits = {
        "Easy": 6,
        "Normal": 8,
        "Hard": 5,
    }
    return limits.get(difficulty, limits["Normal"])


def parse_guess(raw: str, low: int = 1, high: int = 100) -> tuple[bool, int | None, str | None]:
    """Validate and convert a raw text input into an integer guess.

    Args:
        raw: User-entered text from the Streamlit input box.
        low: Minimum allowed guess for the current difficulty.
        high: Maximum allowed guess for the current difficulty.

    Returns:
        A tuple of (is_valid, guess_value, error_message). When the input is
        valid, error_message is None. When invalid, guess_value is None.
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    cleaned = raw.strip()

    try:
        if any(symbol in cleaned.lower() for symbol in [".", "e"]):
            return False, None, "Enter a whole number, not a decimal."
        value = int(cleaned)
    except ValueError:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Please enter a number between {low} and {high}."

    return True, value, None


# FIXME resolved: original AI-generated logic reversed the displayed direction.
# FIX: ChatGPT/Copilot-style review suggested comparing guess and secret directly;
# verified with pytest cases for Too High, Too Low, and Win.
def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Compare the player's guess to the secret and return outcome plus hint."""
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"

    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Return a predictable score update based on the outcome.

    Winning earlier is rewarded more. Incorrect guesses lose one point, which
    keeps the score understandable and avoids the starter code's unpredictable
    score swings.
    """
    if outcome == "Win":
        bonus = max(10, 100 - (attempt_number - 1) * 10)
        return current_score + bonus

    if outcome in {"Too High", "Too Low"}:
        return current_score - 1

    return current_score


def closeness_hint(guess: int, secret: int) -> str:
    """Return a friendly hot/cold hint based on distance from the secret."""
    distance = abs(guess - secret)

    if distance == 0:
        return "🎯 Exact match"
    if distance <= 5:
        return "🔥 Very hot"
    if distance <= 15:
        return "🌡️ Warm"
    return "❄️ Cold"
