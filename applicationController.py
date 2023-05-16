from persona import Person

class applicationController:
  def __init__(self, reader, repo) -> None:
    self.serialReader = reader
    self.repo = repo

  def enrollPerson(self, name: str, phone: str) -> bool:
      id = self.repo.get_all_count() + 1
      person = Person(name, phone)
      if self.serialReader.enrollFinger(id):
        self.repo.add(person, id)

  def verifyPersonData(self, name: str, phone: str) -> bool:
     return name != "" and phone != ""
