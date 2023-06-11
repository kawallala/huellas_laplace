from tinydb import TinyDB, Query
from tinydb.table import Document
from persona import Person

class PersonRepository:
  def __init__(self) -> None:
    self.db = TinyDB('db.json')
    self.person_table = self.db.table('personas')
    self.deleted_table = self.db.table('deleted')
    self.person_query = Query()

  def add(self, person: Person, id: int) -> int:
    self.deleted_table.remove(self.person_query.id == id)
    return self.person_table.insert(Document(vars(person), doc_id=id))

  def get(self, id:int)-> Person:
    result =  self.person_table.get(doc_id = id)
    person = Person(result["name"], result["phone"])
    return person
  
  def delete(self, id: int) -> None:
    self.person_table.remove(doc_ids=[id])
    self.deleted_table.insert({"id": id})
    return 
  
  def get_next_id(self) -> int:
    if len(self.deleted_table.all()) > 0:
      el = self.deleted_table.all()[0]
      return el["id"]
    else:
      return len(self.person_table.all()) + 1
    
  def get_all_count(self) -> int:
    return len(self.db)