from enum import Enum


class Match(Enum):
    EXACT = 1
    MATCH = 0
    NO_MATCH = -1


class Status(Enum):
    WON = 1
    LOST = 0
    IN_PROGRESS = -1


WORD_SIZE = 5
MAX_TRIES = 6


def count_positional_matches(target, guess, letter):
    return len([i for i in range(len(target)) if target[i] == guess[i] == letter])


def count_number_of_occurrences_until_position(position, word, letter):
    return len([i for i in range(position) if word[i] == letter])


def tallyforposition(position, target, guess):
    if target[position] == guess[position]:
        return Match.EXACT

    target_count_occurrences = count_number_of_occurrences_until_position(len(target), target, guess[position])
    positional_matches = count_positional_matches(target, guess, guess[position])
    guess_count_occurrences = count_number_of_occurrences_until_position(position + 1, guess, guess[position])
    target_non_exact_count = target_count_occurrences - positional_matches

    return Match.MATCH if target_non_exact_count >= guess_count_occurrences else Match.NO_MATCH


def verifyGuessLength(target, guess):
    return len(target) != WORD_SIZE or len(guess) != WORD_SIZE


def tally(target, guess):
    if verifyGuessLength(target, guess):
        raise ValueError(target, guess, "Invalid guess")

    return [tallyforposition(i, target, guess) for i in range(len(target))]


def determine_status(response, turns):
    return Status.WON if response == [
        Match.EXACT] * WORD_SIZE else Status.LOST if turns == MAX_TRIES else Status.IN_PROGRESS


def create_message(turns, status, target):
    messages = ["Amazing", "Splendid", "Awesome", "Yay", "Yay", "Yay"]
    return messages[turns - 1] if status == Status.WON else f"It was {target}, better luck next time" if status == Status.LOST else ""


def play(target, readGuess, display):
    for turns in range(1, MAX_TRIES + 1):
        guess = readGuess()
        response = tally(target, guess)
        status = determine_status(response, turns)
        display(turns, status, response, create_message(turns, status, target))
        if status != Status.IN_PROGRESS:
            break
