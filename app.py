import random

import pandas as pd
import streamlit as st

from logic_utils import (
    check_guess,
    closeness_hint,
    get_attempt_limit,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def start_new_game(difficulty: str) -> None:
    """Reset Streamlit session state for a fresh game."""
    low, high = get_range_for_difficulty(difficulty)
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.difficulty = difficulty
    st.session_state.last_message = ""


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("A repaired AI-generated guessing game with tested logic and safer state handling.")

st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)

low, high = get_range_for_difficulty(difficulty)
attempt_limit = get_attempt_limit(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    start_new_game(difficulty)

if st.session_state.get("difficulty") != difficulty:
    start_new_game(difficulty)

st.subheader("Make a guess")
attempts_left = max(0, attempt_limit - st.session_state.attempts)
st.info(f"Guess a number between {low} and {high}. Attempts left: {attempts_left}")

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("Status:", st.session_state.status)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input("Enter your guess:")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_new_game(difficulty)
    st.success("New game started.")
    st.rerun()

if st.session_state.status == "won":
    st.success(
        f"You already won! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}."
    )
elif st.session_state.status == "lost":
    st.error(
        f"Game over. The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}."
    )

if submit and st.session_state.status == "playing":
    # FIXME resolved: invalid guesses used to be processed as real attempts.
    # FIX: AI suggested validating input before touching attempts/score; verified
    # manually with -100, 200, blank input, decimal input, and pytest edge cases.
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.error(err)
    else:
        st.session_state.attempts += 1
        outcome, message = check_guess(guess_int, st.session_state.secret)
        st.session_state.score = update_score(
            st.session_state.score, outcome, st.session_state.attempts
        )

        st.session_state.history.append(
            {
                "Attempt": st.session_state.attempts,
                "Guess": guess_int,
                "Outcome": outcome,
                "Hint": message,
                "Closeness": closeness_hint(guess_int, st.session_state.secret),
                "Score": st.session_state.score,
            }
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.balloons()
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}."
            )
        else:
            if show_hint:
                st.warning(f"{message} {closeness_hint(guess_int, st.session_state.secret)}")

            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}."
                )

if st.session_state.history:
    st.subheader("Guess History")
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)

st.divider()
st.caption("Built by an AI, investigated by a human, and repaired with tests.")
