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
		return chain

	def chains(self):
		if self.track_length < self.chain_size:
			return

		for i in range(self.track_length - self.chain_size - 1):
			yield tuple(self.events_at_position(i))

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
		for event in seed_events:
			gen_events.append(event)
		for i in xrange(size):
			last_event_len = self.chain_size - 1
			last_events = gen_events[-1 * last_event_len:]
			if tuple(last_events) in self.cache:
				next_event = random.choice(self.cache[tuple(last_events)])
				gen_events.append(next_event)
			else:
				seed = random.randint(0, self.track_length - self.chain_size)
				seed_events = self.events_at_position(seed)[:-1]
				for event in seed_events:
					gen_events.append(event)
			
		midi_events = []
		for event in gen_events:
			midi_events.append(event.to_midi_event())
		return midi_events

pattern = midi.read_midifile(sys.argv[1])

location = 0
print pattern
for track in pattern:
	start_of_track = mark_midi.start_of_track(track)
	if start_of_track:
		opening = track[:start_of_track]
		closing = [pattern[1][-1]]
		markov = MidiMarkov(track[start_of_track:-1], 3)
		pattern[location] = opening + markov.generate_markov_text() + closing
	location += 1
#print pattern
# opening = pattern[1][:5]
# closing = [pattern[1][-1]]
# markov = MidiMarkov(pattern[1][-2:4:-1], 4)
# for track in pattern:
# 	opening = pattern[1][:5]
midi.write_midifile(sys.argv[2], pattern)