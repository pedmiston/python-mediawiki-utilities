from .peekable import Peekable

def sequence(*iterables, **kwargs):
	
	compare = kwargs.get('compare', lambda i1,i2:i1<i2)
	iterables = [Peekable(it) for it in iterables]
	
	done = False
	while not done:
		
		next_i = None
		
		for i, it in enumerate(iterables):
			if not it.empty():
				if next_i == None or compare(it.peek(), iterables[next_i].peek()):
					next_i = i
		
		if next_i == None:
			done = True
		else:
			yield iterables[next_i].next()
		
		