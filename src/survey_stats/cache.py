from walrus.tusks.rlite import WalrusLite
from walrus import Database

db = Database('localhost', port=6379, db=0)
rcache = db.cache()
