import midi
import random
import mark_midi
import sys

class MidiMarkov(object):
	def __init__ (self, track, chain_size=3):
		self.chain_size = chain_size
		self.cache = {}
		self.unhashed_track = track
		self.track_length = len(track)
		self.to_hashable_events()
		self.database()

	def to_hashable_events(self):
		self.track = map(mark_midi.to_hashable_event, self.unhashed_track)

	def events_at_position(self, i):
		chain = []
		for chain_index in range(0, self.chain_size):
			chain.append(self.track[i + chain_index])

	def chains(self):
		if self.track_length < self.chain_size:
			return

		for i in range(self.track_length - self.chain_size - 1):
			yield tuple(self.words_at_position(i))

	def database(self):
		for chain_set in self.chains():
			key = chain_set[:self.chain_size - 1]
			next_event = chain_set[-1]
			if key in self.cache:
				self.cache[key].append(next_event)
			else:
				self.cache[key] = [next_event]

	def generate_markov_text(self, size=1):
		size=self.track_length
		seed = random.randint(0, self.track_length - self.chain_size)
		seed_events = self.events_at_position(seed)[:-1]
		gen_events = []
		gen_events.extend(seed_events)
		count = 0
		for i in xrange(size):
			last_event_len = self.chain_size - 1
			last_events = gen_words[-1 * last_event_len:]
			next_event = random.choice(self.cache[tuple(last_worlds)])
			gen_events.append(next_event.to_midi_event())
			# try:
			# 	f1, f2 = e1, e2
			# 	e1, e2 = e2, random.choice(self.cache[(e1, e2)])
			# except:
			# 	seed = random.randint(0, self.track_length-3)
			# 	seed_event, next_event = self.track[seed], self.track[seed+1]
			# 	e1, e2 = seed_event, next_event
		return gen_events

pattern = midi.read_midifile(sys.argv[1])
opening = pattern[1][:5]
closing = [pattern[1][-1]]
markov = MidiMarkov(pattern[1][-2:4:-1], 6)

pattern[1] = opening + markov.generate_markov_text() + closing
midi.write_midifile(sys.argv[2], pattern)