from random import shuffle

colors = ['H', 'T', 'C', 'S']
kinds = ['2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K', 'A']


class Card:
	#(card = Card('2','A'))
	def __init__(self, kind, color):
		self.color = color
		self.kind = kind

	def __str__(self):
		return f'{self.kind} of {self.color}' 
		
class Hand:
	def __init__(self):
		# cards = A of S, 8 of C ...
		self.cards = []

	def __str__(self):
		if not self.cards:
			return '<empty>'
		cards_as_str = ''
		for card in self.cards:
			cards_as_str += f"{str(card)}, \n"
			return cards_as_str

	def clear(self):
		self.cards = []

	def add(self, card):
		self.cards.append(card)

	def give(self, which_hand):
		card = self.cards[0]
		self.cards.remove(card)
		which_hand.add(card)

class Deck(Hand):
	def populate(self):
		populate = []
		for color in colors:
			for kind in kinds:
				card = Card(kind, color)
				populate.append(card)
		self.cards = populate

	def shuffle(self):
		shuffle(self.cards)

	def deal(self, list_of_hands, number_of_cards):
		for hands in range(number_of_cards):
			for hand in list_of_hands:
				this_card = self.cards.pop(0) #bez parametru
				hand.add(this_card)

class Player(Hand):
	def __init__(self, name):
		super().__init__()
		self.name = name
		self.points = 0
		self.busted = False
		self.stopped = False

	def __str__(self):
		cards_value = super().__str__()
		return f'{self.name}: \n{cards_value}POINTS: {self.points}\n'

	def count(self):
		as_in = False
		self.points=0
		for card in self.cards:
			if card.kind == 'A':
				value = 11
				as_in = True
				self.points += value
			elif card.kind in ['K','Q','J']:
				value = 10
				self.points += value
			else:
				value = int(card.kind)
				self.points += value
		if as_in == True and self.points > 20:
			for card in self.cards:
				if card.kind == 'A':
					self.points = self.points - 10
		if self.points >20:
			self.busted = True
			print('BUSTEEEED!')

	def check_player_still_in_game(self):
		if self.stopped == True:
			return False
		if self.busted == True:
			return False
		return True

	def ask(self, deck):
		if not self.busted:
			what_to_do = int(input(f"What's your step {self.name}? \n1 = HIT, \n0= STAND\n"))
			if what_to_do == 1:
				print(f"{self.name} hit a new card!")
				deck.give(self)
			elif what_to_do == 0:
				print(f"{self.name} has standed!")
				self.stopped = True
		

class Croupier(Player):

	def ask(self, deck):
		while not self.busted and not self.stopped:
			if self.points<17:
				deck.give(self)
				self.count()
			else :
				self.stopped = True

		
class BlackJackGame:
	def __init__(self, number_of_players):
		self.players = []
		self.croupier = []

		deck = Deck()
		deck.populate()
		deck.shuffle()

		for i in range(number_of_players):			
			name = input("What's the name of the player: " )
			player = Player(name)
			self.players.append(player)
		
		croupier_name='Croupier'
		croupier = Croupier(croupier_name)
		self.croupier.append(croupier)

		deck.deal(self.players, 2)
		deck.deal(self.croupier, 2)

		for i in range(number_of_players):	
			self.players[i].count()
			print(self.players[i])
		print(f'Croupier \n{croupier.cards[0]}')

		for player in self.players:
			while not player.busted and not player.stopped :
				player.count()
				print(player)
				player.ask(deck)

		croupier.count()
		print(croupier)
		
		should_croupier_ask = 0
		for player in self.players:
			if not player.busted:
				should_croupier_ask += 1

		if should_croupier_ask < 0:
			print('FATALITY! Croupier won with all players!')
		else:
			croupier.ask(deck)

			for player in self.players:
				print(f'{player.name} : {player.points} POINTS')
			print(f'{croupier.name} : {croupier.points} POINTS')
				
			for player in self.players:
				if player.busted:
					print(f'Croupier won with {player.name}')
				elif croupier.points > player.points and croupier.points<21:
					print(f'Croupier won with {player.name}')
				else:
					print(f"{player.name} is a king!")

while True:
	number_of_players = input("How much players will be in the game? Choose the number from 1 to 4: ")
	try:
		number_of_players = int(number_of_players)
	except:
		print('Valid number of players, use only numbers from range. ')
		continue
	if 1 <= number_of_players <= 4:
		break
	else:
		print('Valid range, use a number from interval 1-4')

BlackJackGame = BlackJackGame(int(number_of_players))
