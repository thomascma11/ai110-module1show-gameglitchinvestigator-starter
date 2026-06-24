from logic_utils import (
    check_guess,
    closeness_hint,
    get_attempt_limit,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def test_check_guess_returns_too_low_when_guess_is_below_secret():
    assert check_guess(40, 50) == ("Too Low", "📈 Go HIGHER!")


def test_check_guess_returns_too_high_when_guess_is_above_secret():
    assert check_guess(60, 50) == ("Too High", "📉 Go LOWER!")


def test_check_guess_returns_win_when_correct():
    assert check_guess(50, 50) == ("Win", "🎉 Correct!")


def test_parse_guess_accepts_valid_integer_in_range():
    assert parse_guess("42", 1, 100) == (True, 42, None)


def test_parse_guess_rejects_empty_input():
    ok, value, message = parse_guess("", 1, 100)
    assert ok is False
    assert value is None
    assert message == "Enter a guess."


def test_parse_guess_rejects_non_numeric_input():
    ok, value, message = parse_guess("banana", 1, 100)
    assert ok is False
    assert value is None
    assert message == "That is not a number."


def test_parse_guess_rejects_negative_number():
    ok, value, message = parse_guess("-100", 1, 100)
    assert ok is False
    assert value is None
    assert message == "Please enter a number between 1 and 100."


def test_parse_guess_rejects_number_above_range():
    ok, value, message = parse_guess("101", 1, 100)
    assert ok is False
    assert value is None
    assert message == "Please enter a number between 1 and 100."


def test_parse_guess_rejects_decimal_edge_case():
    ok, value, message = parse_guess("50.5", 1, 100)
    assert ok is False
    assert value is None
    assert message == "Enter a whole number, not a decimal."


def test_update_score_rewards_fast_win():
    assert update_score(0, "Win", 1) == 100


def test_update_score_penalizes_incorrect_guess_predictably():
    assert update_score(0, "Too Low", 1) == -1
    assert update_score(-1, "Too High", 2) == -2


def test_difficulty_ranges_and_attempt_limits():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)
    assert get_attempt_limit("Easy") == 6
    assert get_attempt_limit("Normal") == 8
    assert get_attempt_limit("Hard") == 5


def test_closeness_hint_outputs_expected_labels():
    assert closeness_hint(50, 50) == "🎯 Exact match"
    assert closeness_hint(47, 50) == "🔥 Very hot"
    assert closeness_hint(40, 50) == "🌡️ Warm"
    assert closeness_hint(1, 50) == "❄️ Cold"
