import midi

class HashableEvent(object):
	def __init__(self, tick, channel, data):
		self.tick = tick
		self.channel = channel
		self.data = data

	def __hash__(self):
		print self.tick, self.channel, self.data, self.type
		return hash((self.tick, self.channel, self.data, self.type))

	def __eq__(self, other):
		return (self.tick, self.channel, self.data, self.type) == (other.tick, other.channel, other.data, other.type)


class HashableNoteOnEvent(HashableEvent):
	def __init__(self, tick, channel, data):
		self.type = "Note on"
		super(HashableNoteOnEvent, self).__init__(tick, channel, data)

	def to_midi_event(self):
		return midi.NoteOnEvent(tick=self.tick, channel=self.channel, data=self.data)

class HashableControlChangeEvent(HashableEvent):
	def __init__(self, tick, channel, data):
		self.type = "Control change"
		super(HashableControlChangeEvent, self).__init__(tick, channel, data)

	def to_midi_event(self):
		return midi.ControlChangeEvent(tick=self.tick, channel=self.channel, data=self.data)

def to_hashable_event(event):
	if type(event) == midi.NoteOnEvent:
		return HashableNoteOnEvent(event.tick, event.channel, tuple(event.data))
	else:
		return HashableControlChangeEvent(event.tick, event.channel, tuple(event.data))