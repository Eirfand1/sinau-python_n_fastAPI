class Person:
    def __init__(self, name: str):
        self.name = name

def get_person_name(one_person: Person):
    return one_person.name

orang = Person("Ego")

print(get_person_name(orang))