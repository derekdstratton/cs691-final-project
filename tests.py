import unittest
from gofish import *


class TestGoFish(unittest.TestCase):
    def setUp(self):
        self.deck = ('2 3 4 5 6 7 8 9 10 J Q K A ' * 4).split(' ')
        self.deck.remove('')

    ### Unit Tests

    def test_human_draw_removes_card(self):
        human = HumanPlayer(self.deck)
        initial_deck_length = len(self.deck)
        human.Draw()
        self.assertEqual(initial_deck_length - 1, len(human.deck))

    def test_check_for_books_removes_from_hand(self):
        human = HumanPlayer(self.deck)
        human.hand['K'] = 4
        human.checkForBooks()
        self.assertEqual(human.hand['K'], 0)

    def test_check_for_books_adds_to_score(self):
        human = HumanPlayer(self.deck)
        initial_score = human.score
        human.hand['K'] = 4
        human.checkForBooks()
        self.assertEqual(initial_score + 1, human.score)

    def test_check_empty_draws_if_empty(self):
        human = HumanPlayer(self.deck)
        self.assertEqual(len(human.hand), 0)
        human.emptyCheck()
        self.assertEqual(len(human.hand), 1)

    def test_display_hand_works(self):
        human = HumanPlayer(self.deck)
        human.hand["K"] = 1
        human.hand["3"] = 1
        self.assertEqual(human.displayHand(), "K 3")

    def test_human_fish_for_card_found(self):
        human = HumanPlayer(self.deck)
        human.hand["K"] = 3
        human.hand["Q"] = 3
        self.assertEqual(human.fishFor("K"), 3)
        self.assertEqual(human.hand["K"], 0)

    def test_human_fish_for_card_not_found(self):
        human = HumanPlayer(self.deck)
        human.hand["K"] = 3
        self.assertEqual(human.fishFor("A"), False)

    def test_human_got_card_adds_cards(self):
        human = HumanPlayer(self.deck)
        human.hand["J"] = 1
        human.gotCard("J", 2)
        self.assertEqual(human.hand["J"], 3)

    def test_computer_draw_removes_card(self):
        initial_deck_length = len(self.deck)
        cpu = Computer(self.deck)
        cpu.Draw()
        self.assertEqual(initial_deck_length - 1, len(cpu.deck))

    def test_computer_making_smart_move(self):
        cpu = Computer(self.deck)
        cpu.opponentHas.add('8')
        cpu.hand['8'] = 1
        self.assertEqual(cpu.makeTurn(), '8')

    def test_computer_making_random_move(self):
        cpu = Computer(self.deck)
        cpu.hand['8'] = 1
        self.assertEqual(cpu.makeTurn(), '8')

    def test_computer_fish_for_card_found(self):
        cpu = Computer(self.deck)
        cpu.hand["K"] = 3
        cpu.hand["Q"] = 3
        self.assertEqual(cpu.fishFor("K"), 3)
        self.assertEqual(cpu.hand["K"], 0)

    def test_computer_fish_for_card_not_found(self):
        cpu = Computer(self.deck)
        cpu.hand["K"] = 3
        self.assertEqual(cpu.fishFor("A"), False)

    def test_computer_got_card_adds_cards(self):
        cpu = Computer(self.deck)
        cpu.hand["J"] = 1
        cpu.gotCard("J", 2)
        self.assertEqual(cpu.hand["J"], 3)

    def test_play_game(self):
        game = PlayGoFish()
        # TODO: WRITE INDIVIDUAL TESTS
        game.endOfPlayCheck()
        game.deal_cards()
        game.determine_winner() # test all 3 branches

    ### Integration Tests TODO

