# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

When I first ran the game, the app opened successfully in Streamlit, but the behavior was not trustworthy. The game looked like a normal number guessing game, but the hints and score did not consistently match what happened during play. I used the Developer Debug Info section to compare my guesses against the secret number and confirm that the bugs were real rather than just guesses on my part.

The first major bug was that the hint messages were backwards or misleading. If the guess was higher than the secret number, the user should be told to go lower, but the starter code could show a message telling the player to go higher. The second major bug was that invalid inputs such as `-100`, decimals, and out-of-range numbers were still processed by the game instead of being rejected cleanly. The third major bug was that the score changed in an unpredictable way because the starter scoring logic depended on whether the attempt number was even or odd.

Code-level causes included the `check_guess()` function returning incorrect hint messages, `parse_guess()` not enforcing the active game range, and `update_score()` using confusing parity-based scoring. The starter also mixed game logic directly into `app.py`, which made the bugs harder to isolate and test.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess `60` when the secret is `50` | Game should return `Too High` and tell the user to go lower. | Starter logic could return a misleading upward hint such as `Go HIGHER!`. | No console error; incorrect app output. |
| Guess `-100` on Normal difficulty | Game should reject the input because valid guesses are between 1 and 100. | Starter app accepted the value and continued processing it as game input. | No console error; invalid value appeared in gameplay/history. |
| Guess `50.5` | Game should reject decimals because the game expects whole-number guesses. | Starter parsing converted decimal-looking values using `int(float(raw))`, which changed the user input instead of rejecting it. | No console error; input was silently converted. |
| Several incorrect guesses | Score should update by a clear and predictable rule. | Score could increase or decrease depending on attempt parity, which made it look inconsistent. | No console error; confusing score output. |

---

## 2. How did you use AI as a teammate?

I used AI as a debugging teammate to explain suspicious sections of the code and help plan minimal fixes. One correct AI suggestion was to move pure game logic out of `app.py` and into `logic_utils.py`. That suggestion was correct because functions like `parse_guess()`, `check_guess()`, and `update_score()` do not need Streamlit and can be tested independently with pytest. I verified the suggestion by importing those functions back into `app.py`, running the app manually, and running the automated tests.

Another correct AI suggestion was that the high/low bug should be fixed by comparing the integer guess directly against the integer secret. I verified this with tests where `40` against `50` returns `Too Low`, `60` against `50` returns `Too High`, and `50` against `50` returns `Win`.

One misleading AI suggestion was to rewrite too much of the UI before proving which logic bug caused the wrong hints. That could have introduced new Streamlit bugs while hiding the original problem. I rejected that broad approach and instead made smaller, targeted changes in `logic_utils.py`, then verified each function with simple tests. This helped me stay in control of the debugging process instead of blindly accepting a large AI-generated patch.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed only after checking both the app behavior and the underlying helper function. For the hint bug, I tested `check_guess()` directly with known values so the expected result was obvious. For input validation, I tested blank input, text input, negative numbers, decimals, valid numbers, and numbers above the range.

The automated pytest suite confirmed that the core logic works without relying on the Streamlit interface. For example, `test_check_guess_returns_too_high_when_guess_is_above_secret()` verifies that a guess of `60` against a secret of `50` returns `Too High` and `Go LOWER!`. I also manually ran the Streamlit app and confirmed that invalid guesses do not reduce attempts or update the score.

AI helped me think of edge cases that were easy to miss, especially decimals and out-of-range values. I used those suggestions as a starting point but still checked the tests myself to make sure they matched the intended game rules.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the script from top to bottom whenever a user interacts with a widget. That means regular Python variables can reset unless the app stores important values in `st.session_state`. I would explain it to a friend by saying that Streamlit rebuilds the page after each click, so session state is the app's memory between clicks.

In this project, the secret number, score, attempts, status, and history all needed to live in `st.session_state`. Otherwise, the game could forget the current round or behave like a new game started unexpectedly. I also learned that logic should be separated from UI when possible because pure logic functions are much easier to test.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing small tests for the exact behavior I am trying to fix. The test cases made the debugging process less emotional because I could prove whether the code worked. I also want to keep using bug reproduction tables because they force me to connect an input, expected behavior, actual behavior, and evidence.

Next time I work with AI on a coding task, I would ask for smaller patches earlier instead of asking for broad rewrites. This project changed the way I think about AI-generated code because I saw that AI can produce code that looks confident but still has real logic bugs. AI is helpful, but the developer still has to verify the result.
