from tinydb import TinyDB, Query
from tinydb.table import Document

class PersonRepository:
  def __init__(self) -> None:
    self.db = TinyDB('db.json')
  
  def add(self, person):
    self.db.insert(Document(vars(person), doc_id=person.id))

  def get_all_count(self):
    return len(self.db.all())