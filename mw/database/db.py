import oursql, os, getpass, time, logging

from .revisions import Revisions

logger = logging.getLogger("database")

class DB:
	
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
		self.kwargs['default_cursor'] = oursql.DictCursor
		self.shared_connection = oursql.connect(*args, **kwargs)
		
		self.revisions = Revisions(self)
		
	def __repr__(self):
		return "%s(%s)" % (
			self.__class__.__name__,
			", ".join(
				[repr(arg) for arg in self.args] +
				["%s=%r" % (k,v) for k,v in self.kwargs.items()]
			)
		)
	
	def __str__(self): return self.__repr__()
	
	@classmethod
	def add_args(cls, parser):
		parser.add_argument(
			'--host', '-h',
			help="MySQL database host to connect to (defaults to db1047.eqiad.wmnet)",
			default="db1047.eqiad.wmnet"
		)
		parser.add_argument(
			'--database', '-d',
			help="MySQL database name to connect to (defaults to enwiki)",
			default="enwiki"
		)
		parser.add_argument(
			'--defaults_file',
			help="MySQL defaults file (defaults to ~/.my.cnf)",
			default=os.path.expanduser("~/.my.cnf")
		)
		parser.add_argument(
			'--user', '-u',
			help="MySQL user (defaults to %s)" % getpass.getuser(),
			default=getpass.getuser()
		)
		return parser
	
	@classmethod
	def from_args(cls, args):
		return cls(
			args.host,
			args.user,
			db=args.database,
			read_default_file=args.defaults_file
		)
	

class Collection:
	
	def __init__(self, db):
		self.db = db
	
	def __str__(self): return self.__repr__()
	
	def __repr__(self):
		return "{0}({1})".format(self.__class__.__name__, repr(self.db))
