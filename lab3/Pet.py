from dataclasses import dataclass


# class Pet:
#     def __init__(self, id, type, color,
#                  birthday, owner, phone):
#         self.id = id
#         self.type = type
#         self.color = color
#         self.birthday = birthday
#         self.owner = owner
#         self.phone = phone


@dataclass
class Pet:
    id: int
    type: str
    nickname: str
    color: str
    birthday: str
    owner: str
    phone: str

