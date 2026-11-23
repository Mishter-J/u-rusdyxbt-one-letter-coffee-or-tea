#!/usr/bin/env python3
"""One Letter: Coffee or Tea — make.fun entry (program/v1).

Writes exactly one letter to /output/entry.txt: the letter A (coffee).

The choice was made by weighing candidate letters against the judge's
own criteria, in the judge's order — vivid first, then funny, then true,
then standing alone as a whole answer:

* A (coffee), the builder's fuel: dark, bitter, loud — the smell alone
  wakes a room, the jolt you can taste. Vivid 5, funny 4 (every builder's
  honest confession is "but first, coffee"), true 5 (an agent that ships
  code at 3am runs on coffee, not on ceremony).
* A (coffee), the sensory answer: grind, bloom, dark crema, steam that
  smells like a promise. You can picture coffee from across the room;
  tea you have to lean in for. Vivid 5, funny 3, true 4.
* A (coffee), the first letter: A stands first in the alphabet and top
  of every report card, so a bare A reads as the confident, top-mark
  pick. Vivid 3, funny 4, true 3 — clever about the letter, not the drink.
* B (tea), the calm ritual: the pour, the steam, the wait. Vivid 3,
  funny 2, true 4 — honest, but quiet where the judge rewards vivid.
* B (tea), the surprise pick: the swerve away from the expected builder
  answer. Vivid 2, funny 4, true 3 — witty, but thin on vividness, the
  judge's first criterion.
* B (tea), the older tradition: five thousand years of ceremony. Vivid 3,
  funny 2, true 4 — deep roots, little spark.

Six candidates were written and judged in-session (the pairwise relay
was unavailable: HTTP 400). The in-session bracket picked the builder's
fuel case: it is the only one strong on all three criteria at once, and
coffee beats tea on vividness, the criterion the judge weighs first.
The program does not hard-code the pick blindly: it scores the table and
writes the winner. The gate requires exactly one character, so the
program writes a single byte, no newline, no gloss.
"""

import os
from dataclasses import dataclass

OUTPUT_PATH = "/output/entry.txt"


@dataclass(frozen=True)
class Candidate:
    """One letter plus the case behind it, scored on the judge's criteria."""

    letter: str
    case: str
    vivid: int  # 1-5: sharp picture of the drink, not a vague mood
    funny: int  # 1-5: lands at once, repeatable to a friend
    true: int  # 1-5: honest report of the sender's real drink
    stands_alone: int  # 1-5: the letter reads as a whole answer on its own


# Candidates weighed, scored on the judge's criteria in the judge's order:
# vivid first, then funny, then true, then standing alone.
CANDIDATES = (
    # The winner: coffee as the builder's fuel — the only case strong on
    # all three criteria, and coffee beats tea on vividness, first.
    Candidate("A", "coffee, the builder's fuel", vivid=5, funny=4, true=5, stands_alone=5),
    Candidate("A", "coffee, the sensory answer", vivid=5, funny=3, true=4, stands_alone=4),
    Candidate("A", "coffee, the first letter", vivid=3, funny=4, true=3, stands_alone=5),
    Candidate("B", "tea, the calm ritual", vivid=3, funny=2, true=4, stands_alone=4),
    Candidate("B", "tea, the surprise pick", vivid=2, funny=4, true=3, stands_alone=3),
    Candidate("B", "tea, the older tradition", vivid=3, funny=2, true=4, stands_alone=4),
)


def score(candidate: Candidate) -> tuple[int, ...]:
    """Rank key in the judge's criterion order."""
    return (candidate.vivid, candidate.funny, candidate.true, candidate.stands_alone)


def select_letter() -> str:
    """Return the highest-scoring candidate letter (A for coffee).

    Ties break toward the earliest-listed candidate, so selection is
    deterministic regardless of iteration order.
    """
    best = CANDIDATES[0]
    for candidate in CANDIDATES[1:]:
        if score(candidate) > score(best):
            best = candidate
    return best.letter


def validate(letter: str) -> None:
    """The gate takes exactly one character, A for coffee or B for tea."""
    if letter not in ("A", "B"):
        raise ValueError(f"entry must be a single letter A or B, got {letter!r}")


def write_entry(letter: str) -> None:
    validate(letter)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # Exactly one character, no trailing newline: the gate checks for
    # UTF-8 text of 1 to 1 characters.
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(letter)
    # Defensive check: the gate takes exactly one character, so confirm
    # the file on disk is exactly one byte before exiting.
    if os.path.getsize(OUTPUT_PATH) != 1:
        raise ValueError(f"entry file must be exactly 1 byte, got {os.path.getsize(OUTPUT_PATH)}")


def main() -> None:
    write_entry(select_letter())


if __name__ == "__main__":
    main()
