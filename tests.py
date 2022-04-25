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
        game.determine_winner() # test all 3 branches

    def test_nine_cards_are_dealt_to_each(self):
        game = PlayGoFish()
        game.deal_cards()
        # 34 cards remain in the deck: 54 - 18 (9 cards for 2 players)
        self.assertEqual(len(game.deck), 34)

    def test_human_wins(self):
        game = PlayGoFish()
        game.player[0].score = 2
        game.player[1].score = 1
        # player 0 is human
        self.assertEqual(game.determine_winner(), 0)

    def test_computer_wins(self):
        game = PlayGoFish()
        game.player[0].score = 1
        game.player[1].score = 2
        # player 1 is cpu
        self.assertEqual(game.determine_winner(), 1)

    def test_game_is_draw(self):
        game = PlayGoFish()
        game.player[0].score = 2
        game.player[1].score = 2
        # draw is -1
        self.assertEqual(game.determine_winner(), -1)

    ### Integration Tests

    def test_cpu_gives_requested_card_to_player(self):
        cpu = Computer(self.deck)
        # cpu has 2 aces and 1 2
        cpu.hand["A"] = 2
        cpu.hand["2"] = 1
        human = HumanPlayer(self.deck)
        # human has 1 ace
        human.hand["A"] = 1
        game = PlayGoFish()
        game.player[0] = human
        game.player[1] = cpu
        # human asks cpu for A, and should give over 2
        game.card_interaction(0, 1, 'A')
        self.assertEqual(game.player[0].hand["A"], 3)
        self.assertEqual(game.player[1].hand["A"], 0)

    def test_cpu_doesnt_have_card_and_player_fishes(self):
        # put a 6 at the end of the deck so the player always draws this
        self.deck.append('6')
        cpu = Computer(self.deck)
        # cpu has 2 aces
        cpu.hand["A"] = 2
        human = HumanPlayer(self.deck)
        # human has 1 jack
        human.hand["J"] = 1
        game = PlayGoFish()
        game.player[0] = human
        game.player[1] = cpu
        # human asks cpu for J, and should fish and add a card to hand
        game.card_interaction(0, 1, 'J')
        self.assertEqual(game.player[0].hand["J"], 1)
        self.assertEqual(game.player[0].hand["6"], 1)
        self.assertEqual(game.player[1].hand["A"], 2)

    def test_human_gives_requested_card_to_cpu(self):
        cpu = Computer(self.deck)
        # cpu has 1 ace
        cpu.hand["A"] = 1
        human = HumanPlayer(self.deck)
        # human has 2 aces and 1 2
        human.hand["A"] = 2
        human.hand["2"] = 1
        game = PlayGoFish()
        game.player[0] = human
        game.player[1] = cpu
        # cpu asks human for A, and should give over 2
        game.card_interaction(1, 0, 'A')
        self.assertEqual(game.player[1].hand["A"], 3)
        self.assertEqual(game.player[0].hand["A"], 0)

    def test_human_doesnt_have_card_and_cpu_fishes(self):
        # put a 6 at the end of the deck so the cpu always draws this
        self.deck.append('6')
        cpu = Computer(self.deck)
        # cpu has 2 aces
        cpu.hand["A"] = 2
        human = HumanPlayer(self.deck)
        # human has 1 jack
        human.hand["J"] = 1
        game = PlayGoFish()
        game.player[0] = human
        game.player[1] = cpu
        # cpu asks human for A, and should fish and add a card to hand
        game.card_interaction(1, 0, 'A')
        self.assertEqual(game.player[0].hand["J"], 1)
        self.assertEqual(game.player[1].hand["6"], 1)
        self.assertEqual(game.player[1].hand["A"], 2)

    def test_deck_and_all_hands_are_empty_so_game_ends(self):
        game = PlayGoFish()
        game.deck = []  # empty decks
        cpu = Computer(game.deck)
        human = HumanPlayer(game.deck)
        # no cards initialized in their hands
        game.player[0] = human
        game.player[1] = cpu
        self.assertFalse(game.endOfPlayCheck())

    def test_deck_has_cards_so_game_continues(self):
        game = PlayGoFish()
        game.deck = ['1']
        cpu = Computer(game.deck)
        human = HumanPlayer(game.deck)
        # no cards initialized in their hands
        game.player[0] = human
        game.player[1] = cpu
        self.assertTrue(game.endOfPlayCheck())