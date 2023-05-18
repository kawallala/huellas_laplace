from tinydb import TinyDB, Query
from tinydb.table import Document
from persona import Person

class PersonRepository:
  def __init__(self) -> None:
    self.db = TinyDB('db.json')
    self.personQuery = Query()

  def add(self, person: Person, id: int) -> int:
    return self.db.insert(Document(vars(person), doc_id=id))

  def get(self, id:int)-> Person:
    result =  self.db.get(doc_id = id)
    person = Person(result["name"], result["phone"])
    return person
  
  def get_all_count(self) -> int:
    return len(self.db)