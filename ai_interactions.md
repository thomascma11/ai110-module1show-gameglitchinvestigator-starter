# AI Interactions Log

## Agent Workflow

**What task did you give the agent?**

I asked the AI coding assistant to help refactor the guessing game's pure logic out of `app.py` and into `logic_utils.py`, then repair the high/low hint bug and input validation bug.

**What did the agent do?**

The AI identified that `parse_guess()`, `check_guess()`, `update_score()`, and difficulty helpers were better suited for `logic_utils.py`. It suggested importing those helpers back into `app.py` so the Streamlit file could focus on UI and session state.

**Files modified:**

- `logic_utils.py`
- `app.py`
- `tests/test_game_logic.py`
- `README.md`
- `reflection.md`

**What did you have to verify or fix manually?**

I manually verified that the hint direction matched the comparison. I also rejected a broad UI rewrite suggestion because it changed too much before proving the root cause. I kept the final code focused on direct comparisons, input validation, predictable scoring, and testable helper functions.

---

## Test Generation: Advanced Edge-Case Testing

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative number | `Generate pytest cases for invalid guessing-game inputs such as negative values.` | `parse_guess("-100", 1, 100)` should return invalid. | Yes | Negative guesses are outside every game range and should not count as real attempts. |
| Decimal input | `Generate edge-case tests for decimals and non-whole-number input.` | `parse_guess("50.5", 1, 100)` should return invalid. | Yes | The game asks for a whole-number guess, so silently converting decimals would misrepresent user input. |
| Non-numeric string | `Generate tests for non-numeric user input in parse_guess.` | `parse_guess("banana", 1, 100)` should return invalid. | Yes | Text input should show a helpful error rather than crash or update game state. |
| Out-of-range high value | `Generate tests for guesses outside the selected difficulty range.` | `parse_guess("101", 1, 100)` should return invalid. | Yes | Values above the maximum should not affect attempts or score. |

---

## Linting & Style

**Prompt used:**

```text
Review logic_utils.py for readability, PEP 8 style, and docstrings. Keep the suggestions minimal and do not change the public behavior.
```

**Linting output before:**

```text
No formal linter was required for this assignment. Manual review found missing function docstrings in the starter logic_utils.py and UI/game logic mixed together in app.py.
```

**Changes applied:**

I added docstrings to every function in `logic_utils.py`, used descriptive helper names, kept line lengths readable, and separated pure logic from Streamlit UI code. I also used explicit return types for the main helper functions.

---

## Enhanced Game UI

**Enhancement added:**

I added a guess history table to the Streamlit app. The table shows each valid attempt, the guess, the outcome, the hint, the hot/cold closeness label, and the score after that attempt.

**Relevant functions/code sections:**

- `closeness_hint()` in `logic_utils.py`
- `st.session_state.history` in `app.py`
- `st.dataframe(...)` in `app.py`

**Why it improves the game:**

The history table makes the game easier to understand because the player can see the round's progress instead of relying only on the latest message.

---

## Model / Prompt Comparison

**Task given to both approaches:**

Fix the high/low hint bug in the guessing game.

| | Model / Prompt A | Model / Prompt B |
|-|------------------|------------------|
| **Approach** | Broad prompt: “Fix the game.” | Targeted prompt: “Fix only the check_guess high/low comparison bug.” |
| **Response summary** | Suggested many UI and state changes at once. | Focused on comparing guess and secret directly. |
| **More Pythonic?** | Less Pythonic because it changed too much at once. | More Pythonic because it used a small pure function. |
| **Clearer explanation?** | Less clear because many changes were bundled together. | Clearer because the cause and fix were easy to verify. |

**Which did you prefer and why?**

I preferred the targeted prompt because it produced a smaller fix that was easier to test. It also helped me avoid blindly accepting a broad rewrite.
