from models.general import RoleType
from tests.functional.utils.hash import hash_password

users_data = [
    ('16bdbb16-d3bf-4184-b08e-e2b2eabeee7f', 'ivan', hash_password('ivanivanov'), RoleType.STANDARD.name),
    ('15e794ed-2286-4690-b092-793f5e51f0ec', 'liza', hash_password('LKjj78!ksjd'), RoleType.STANDARD.name),
    ('bb81ead9-b728-461b-a0a9-eacc9b7127a2', 'oleg', hash_password('Ldfj78!ksjd'), RoleType.PRIVILEGED.name),
    ('e2da75c0-8f07-4d20-bfc4-8afcf58e7a2c', 'admin', hash_password('adminADMINOV1!'), RoleType.ADMIN.name)
]
