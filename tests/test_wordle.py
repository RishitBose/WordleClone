import unittest 
from src import Wordle as Wordle
from src.Wordle import Match
from src.Wordle import Status


class WordleTest(unittest.TestCase):
    def test_canary(self):
        self.assertTrue(True)

    def test_tally(self):
        test_sample = [
            ["FAVOR", "FAVOR", [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT]],
            ["FAVOR", "TESTS", [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH]],
            ["FAVOR", "RAPID", [Match.MATCH, Match.EXACT, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH]],
            ["FAVOR", "MAYOR", [Match.NO_MATCH, Match.EXACT, Match.NO_MATCH, Match.EXACT, Match.EXACT]],
            ["FAVOR", "RIVER", [Match.NO_MATCH, Match.NO_MATCH, Match.EXACT, Match.NO_MATCH, Match.EXACT]],
            ["FAVOR", "AMAST", [Match.MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH]],
            ["SKILL", "SKILL", [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT]],
            ["SKILL", "SWIRL", [Match.EXACT, Match.NO_MATCH, Match.EXACT, Match.NO_MATCH, Match.EXACT]],
            ["SKILL", "CIVIL", [Match.NO_MATCH, Match.MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.EXACT]],
            ["SKILL", "SHIMS", [Match.EXACT, Match.NO_MATCH, Match.EXACT, Match.NO_MATCH, Match.NO_MATCH]],
            ["SKILL", "SILLY", [Match.EXACT, Match.MATCH, Match.MATCH, Match.EXACT, Match.NO_MATCH]],
            ["SKILL", "SLICE", [Match.EXACT, Match.MATCH, Match.EXACT, Match.NO_MATCH, Match.NO_MATCH]],
            ["SAGAS", "ABASE", [Match.MATCH, Match.NO_MATCH, Match.MATCH, Match.MATCH, Match.NO_MATCH]]
        ]
      
        for target, guess, expected_response in test_sample:
            with self.subTest(msg = f"tally if guess {guess} matches target {target}"):
                self.assertEqual(expected_response, Wordle.tally(target, guess))
      
    def test_tally_invalid_guess(self):
        test_sample = [
            ["FAVOR", "FOR", ValueError],
            ["FAVOR", "FERVER", ValueError],
            ["RIDDLE", "RIDDLE", ValueError]
        ]
        
        for target, guess, expected_response in test_sample:
            with self.subTest(msg = f"tally if guess {guess} matches target {target}"):
                with self.assertRaises(expected_response):
                    Wordle.tally(target, guess)
    
    def test_play_first_attempt_correct_guess(self):
        def readGuess():
            return "FAVOR"
            
        displayCalled = False
        def display(numAttempts, status, tallyOutput, finalMessage):
            self.assertEqual([numAttempts, status, tallyOutput, finalMessage], [1, Status.WON, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], "Amazing"])
            nonlocal displayCalled
            displayCalled = True
            
        Wordle.play("FAVOR", readGuess, display)

        self.assertTrue(displayCalled)
    
    
    def test_play_first_attempt_invalid_guess(self):
        def readGuess():
            return "FOR"

        with self.assertRaises(ValueError):
            Wordle.play("FAVOR", readGuess, None)
    
    def test_play_first_attempt_wrong_guess(self):
        def readGuess():
            return "SKILL"
            
        displayCalled = False
                    
        def display(numAttempts, status, tallyOutput, finalMessage):
            if numAttempts == 1:
              self.assertEqual([numAttempts, status, tallyOutput, finalMessage], [1, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH], ""])
              nonlocal displayCalled
              displayCalled = True
            
        Wordle.play("FAVOR", readGuess, display)

        self.assertTrue(displayCalled)
    
    def test_play_second_attempt_correct_guess(self):
        guesses = ["FAVOR", "SMILE"]
        
        def readGuess():
            return guesses.pop()
            
        displayCallCount = 0
        expectedResults = [
          [2, Status.WON, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], "Splendid"],
          [1, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH], ""],
        ]
        
        def display(numAttempts, status, tallyOutput, finalMessage):
            self.assertEqual([numAttempts, status, tallyOutput, finalMessage], expectedResults.pop())
            nonlocal displayCallCount
            displayCallCount += 1
            
        Wordle.play("FAVOR", readGuess, display)

        self.assertEqual(2, displayCallCount)
    
    def test_play_second_attempt_wrong_guess(self):
        guesses = ["SKILL", "RAPID"]
        def readGuess():
            return guesses.pop()

        displayCallCount = 0
        expectedResults = [
            [2, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH], ""],
            [1, Status.IN_PROGRESS, [Match.MATCH, Match.EXACT, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH], ""],
        ]
        
        def display(numAttempts, status, tallyOutput, finalMessage):
            if numAttempts <= 2:
                self.assertEqual([numAttempts, status, tallyOutput, finalMessage], expectedResults.pop())
            nonlocal displayCallCount
            displayCallCount += 1
        
        with self.assertRaises(IndexError):
            Wordle.play("FAVOR", readGuess, display)
            
        self.assertEqual(2, displayCallCount)

    def test_play_third_attempt_correct_guess(self):
        guesses = ["FAVOR", "SMILE", "SKILL"]

        def readGuess():
            return guesses.pop()

        displayCallCount = 0
        expectedResults = [
            [3, Status.WON, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], "Awesome"],
            [2, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH], ""],
            [1, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH],
             ""],
        ]

        def display(numAttempts, status, tallyOutput, finalMessage):
            self.assertEqual([numAttempts, status, tallyOutput, finalMessage], expectedResults.pop())
            nonlocal displayCallCount
            displayCallCount += 1

        Wordle.play("FAVOR", readGuess, display)

        self.assertEqual(3, displayCallCount)

    def test_play_fourth_attempt_correct_guess(self):
        guesses = ["FAVOR", "THORN", "SMILE", "SKILL"]

        def readGuess():
            return guesses.pop()

        displayCallCount = 0
        expectedResults = [
            [4, Status.WON, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], "Yay"],
            [3, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.MATCH, Match.MATCH, Match.NO_MATCH], ""],
            [2, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH], ""],
            [1, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH],
             ""],
        ]

        def display(numAttempts, status, tallyOutput, finalMessage):
            self.assertEqual([numAttempts, status, tallyOutput, finalMessage], expectedResults.pop())
            nonlocal displayCallCount
            displayCallCount += 1

        Wordle.play("FAVOR", readGuess, display)

        self.assertEqual(4, displayCallCount)
        
    def test_play_fifth_attempt_correct_guess(self):
        guesses = ["FAVOR", "ABASE", "THORN", "SMILE", "SKILL"]

        def readGuess():
            return guesses.pop()

        displayCallCount = 0
        expectedResults = [
            [5, Status.WON, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], "Yay"],
            [4, Status.IN_PROGRESS, [Match.MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH], ""],
            [3, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.MATCH, Match.MATCH, Match.NO_MATCH], ""],
            [2, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH], ""],
            [1, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH],
             ""],
        ]

        def display(numAttempts, status, tallyOutput, finalMessage):
            self.assertEqual([numAttempts, status, tallyOutput, finalMessage], expectedResults.pop())
            nonlocal displayCallCount
            displayCallCount += 1

        Wordle.play("FAVOR", readGuess, display)

        self.assertEqual(5, displayCallCount)
    
    def test_play_sixth_attempt_correct_guess(self):
        guesses = ["FAVOR", "SAVOR", "ABASE", "THORN", "SMILE", "SKILL"]

        def readGuess():
            return guesses.pop()

        displayCallCount = 0
        expectedResults = [
            [6, Status.WON, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], "Yay"],
            [5, Status.IN_PROGRESS, [Match.NO_MATCH, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], ""],
            [4, Status.IN_PROGRESS, [Match.MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH], ""],
            [3, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.MATCH, Match.MATCH, Match.NO_MATCH], ""],
            [2, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH], ""],
            [1, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH],
             ""],
        ]

        def display(numAttempts, status, tallyOutput, finalMessage):
            self.assertEqual([numAttempts, status, tallyOutput, finalMessage], expectedResults.pop())
            nonlocal displayCallCount
            displayCallCount += 1

        Wordle.play("FAVOR", readGuess, display)

        self.assertEqual(6, displayCallCount)
    
    def test_play_sixth_attempt_wrong_guess(self):
        guesses = ["GUESS", "SAVOR", "ABASE", "THORN", "SMILE", "SKILL"]

        def readGuess():
            return guesses.pop()

        displayCallCount = 0
        expectedResults = [
            [6, Status.LOST, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH], "It was FAVOR, better luck next time"],
            [5, Status.IN_PROGRESS, [Match.NO_MATCH, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], ""],
            [4, Status.IN_PROGRESS, [Match.MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH], ""],
            [3, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.MATCH, Match.MATCH, Match.NO_MATCH], ""],
            [2, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH], ""],
            [1, Status.IN_PROGRESS, [Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH, Match.NO_MATCH],
             ""],
        ]

        def display(numAttempts, status, tallyOutput, finalMessage):
            self.assertEqual([numAttempts, status, tallyOutput, finalMessage], expectedResults.pop())
            nonlocal displayCallCount
            displayCallCount += 1

        Wordle.play("FAVOR", readGuess, display)

        self.assertEqual(6, displayCallCount)
        
    def test_verify_readGuess_Not_Called_After_Second_Attempt_Win(self):
        guesses = ["FAVOR", "SMILE"]
        
        readGuessCallCount = 0
        
        def readGuess():
            nonlocal readGuessCallCount
            readGuessCallCount += 1
            return guesses.pop()
        
        def display(numAttempts, status, tallyOutput, finalMessage):
            pass
            
        Wordle.play("FAVOR", readGuess, display)
        self.assertEqual(2, readGuessCallCount)
    
    def test_verify_readGuess_Not_Called_After_Sixth_Attempt_Loss(self):
        guesses = ["GUESS", "SAVOR", "ABASE", "THORN", "SMILE", "SKILL"]
        
        readGuessCallCount = 0

        def readGuess():
            nonlocal readGuessCallCount
            readGuessCallCount += 1
            return guesses.pop()

        def display(numAttempts, status, tallyOutput, finalMessage):
            pass

        Wordle.play("FAVOR", readGuess, display)

        self.assertEqual(6, readGuessCallCount)
        
if __name__ == '__main__':
	unittest.main()
