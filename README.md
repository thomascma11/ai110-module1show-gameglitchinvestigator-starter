# 🎮 Game Glitch Investigator: Repaired Glitchy Guesser

## Project Overview

This project repairs an AI-generated Streamlit number guessing game. The starter version looked simple, but it had several real bugs: misleading hints, unpredictable score changes, invalid inputs being processed as guesses, and game logic mixed directly into the UI file.

The final version separates core logic into `logic_utils.py`, keeps Streamlit UI/state handling in `app.py`, and verifies the repaired behavior with pytest.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python -m streamlit run app.py
```

Run tests:

```bash
python -m pytest
```

## Game Purpose

The game chooses a secret number based on the selected difficulty level. The player enters guesses until they either find the correct number or run out of attempts. The app provides direction hints, a score, and a guess history table so the player can understand what happened during the round.

## Bugs Found

### Bug 1: Hint directions were misleading

The starter code returned messages that did not match the comparison result. For example, when a guess was higher than the secret number, the game could display a message telling the player to go higher instead of lower.

**Fix:** `check_guess()` now compares integers directly and returns the correct direction:

- Guess below secret → `Too Low`, `Go HIGHER`
- Guess above secret → `Too High`, `Go LOWER`
- Guess equals secret → `Win`

### Bug 2: Invalid inputs were processed as real guesses

The game accepted values like `-100`, decimals, and values outside the selected difficulty range. These inputs could still affect attempts/history and make the game behavior confusing.

**Fix:** `parse_guess()` now validates blank input, non-numeric input, decimals, negative numbers, and out-of-range values before the app updates attempts or score.

### Bug 3: Score behavior was unpredictable

The starter scoring logic changed score differently depending on attempt parity, which made the score feel random and difficult to explain.

**Fix:** `update_score()` now uses predictable rules: incorrect guesses lose 1 point, and winning earns a larger bonus based on how early the user wins.

### Bug 4: UI and game logic were mixed together

The starter `app.py` contained parsing, guess checking, scoring, difficulty setup, and UI code all in one file. This made the logic harder to test.

**Fix:** Core game logic was refactored into `logic_utils.py`, while `app.py` now focuses on Streamlit UI and session state.

## Demo Walkthrough

1. User starts the game on **Normal** difficulty.
2. App displays the range: `1 to 100` and attempts allowed: `8`.
3. User enters `-100`.
4. Game returns: `Please enter a number between 1 and 100.` The guess is not counted as a real attempt.
5. User enters `40` while the secret is `50`.
6. Game returns: `Too Low` / `Go HIGHER!` and records the guess in the guess history table.
7. User enters `60` while the secret is `50`.
8. Game returns: `Too High` / `Go LOWER!`.
9. User enters `50`.
10. Game returns `Correct`, shows the win message, updates the score, and stops the round until a new game starts.

## Enhanced UI Changes

I added a structured guess history table in `app.py` using the `history` session-state list. Each valid guess records:

- Attempt number
- Guess
- Outcome
- Hint
- Hot/cold closeness label
- Score after the guess

I also added the `closeness_hint()` function in `logic_utils.py` to make feedback more user-friendly with labels such as `🔥 Very hot`, `🌡️ Warm`, and `❄️ Cold`.

## Test Results

```text
============================= test session starts =============================
platform win32 -- Python 3.13.0, pytest-8.4.1, pluggy-1.6.0
rootdir: C:\Users\ocdde\Downloads\ai110-module1show-gameglitchinvestigator-starter
collected 13 items

tests/test_game_logic.py .............                                  [100%]

============================== 13 passed in 0.13s ==============================
```

## Files Included

- `app.py` — Streamlit UI, session state, and game flow
- `logic_utils.py` — testable game logic functions
- `tests/test_game_logic.py` — automated pytest coverage
- `reflection.md` — bug logs and AI collaboration reflection
- `ai_interactions.md` — stretch documentation for edge-case testing, style, and UI improvements
- `test_results.txt` — copied pytest output
- `requirements.txt` — required packages

## AI Collaboration Summary

I used AI assistance to explain the broken comparison logic, suggest refactoring logic into `logic_utils.py`, and generate pytest cases. I did not accept every suggestion automatically. Some suggestions were too broad and tried to change the UI before confirming the actual logic bug, so I kept the final fixes targeted and verified each change through manual gameplay and automated tests.
