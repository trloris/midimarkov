import midi
import random
import mark_midi
import sys

class MidiMarkov(object):
	def __init__ (self, track):
		self.cache = {}
		self.unhashed_track = track
		self.track_length = len(track)
		self.to_hashable_events()
		self.database()

	def to_hashable_events(self):
		self.track = map(mark_midi.to_hashable_event, self.unhashed_track)

	def triples(self):
		if self.track_length < 3:
			return

		for i in range(self.track_length - 2):
			yield (self.track[i], self.track[i+1], self.track[i+2])

	def database(self):
		for e1, e2, e3 in self.triples():
			key = (e1, e2)
			if key in self.cache:
				self.cache[key].append(e3)
			else:
				self.cache[key] = [e3]

	def generate_markov_text(self, size=1):
		size=self.track_length
		seed = random.randint(0, self.track_length-3)
		seed_event, next_event = self.track[seed], self.track[seed+1]
		e1, e2 = seed_event, next_event
		gen_events = []
		count = 0
		for i in xrange(size):
			gen_events.append(e1.to_midi_event())
			try:
				f1, f2 = e1, e2
				e1, e2 = e2, random.choice(self.cache[(e1, e2)])
			except:
				seed = random.randint(0, self.track_length-3)
				seed_event, next_event = self.track[seed], self.track[seed+1]
				e1, e2 = seed_event, next_event
			count = count + 1
			gen_events.append(e2.to_midi_event())
		return gen_events

pattern = midi.read_midifile(sys.argv[1])
opening = pattern[1][:5]
closing = [pattern[1][-1]]
markov = MidiMarkov(pattern[1][-2:4:-1])

pattern[1] = opening + markov.generate_markov_text() + closing
midi.write_midifile(sys.argv[2], pattern)