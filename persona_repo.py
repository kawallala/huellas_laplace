from tinydb import TinyDB, Query
from tinydb.table import Document
from persona import Person

class PersonRepository:
    def __init__(self, app_logger) -> None:
        self.db = TinyDB('db.json')
        self.person_table = self.db.table('personas')
        self.deleted_table = self.db.table('deleted')
        self.person_query = Query()
        self.app_logger = app_logger

    def add(self, person: Person, id: int) -> int:
        self.deleted_table.remove(self.person_query.id == id)
        new_person_id = self.person_table.insert(Document(vars(person), doc_id=id))
        self.app_logger.info(f'Persona agregada: {person} con ID: {new_person_id}')
        return new_person_id

    def get(self, id: int) -> Person:
        result = self.person_table.get(doc_id=id)
        person = Person(result["name"], result["phone"])
        self.app_logger.debug(f'Persona obtenida con ID: {id}')
        return person

    def delete(self, id: int) -> None:
        self.person_table.remove(doc_ids=[id])
        self.deleted_table.insert({"id": id})
        self.app_logger.warning(f'Persona eliminada con ID: {id}')

    def get_next_id(self) -> int:
        if len(self.deleted_table.all()) > 0:
            el = self.deleted_table.all()[0]
            next_id = el["id"]
            self.app_logger.info(f'ID disponible para reutilizar: {next_id}')
            return next_id
        else:
            next_id = len(self.person_table.all()) + 1
            self.app_logger.info(f'ID generado para nueva persona: {next_id}')
            return next_id

    def get_all_count(self) -> int:
        count = len(self.db)
        self.app_logger.debug(f'Cantidad total de personas en la base de datos: {count}')
        return count

    def get_all(self):
        all_persons = self.person_table.all()
        self.app_logger.debug('Obtenidas todas las personas de la base de datos')
        return all_persons