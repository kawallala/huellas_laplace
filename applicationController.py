from serialService import SerialReader
from personaRepo import PersonRepository
from persona import Person

class applicationController:
  def __init__(self) -> None:
    self.serialReader = SerialReader()
    self.repo = PersonRepository()

  def enrollPerson(self, name: str, phone: str) -> bool:
      id = self.repo.get_all_count() + 1
      person = Person(name, phone)
      if self.serialReader.enrollFinger(id):
        self.repo.add(person, id)
