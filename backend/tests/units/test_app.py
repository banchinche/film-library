# import datetime
# from backend.project import models
# from werkzeug.security import generate_password_hash, check_password_hash
# import pytest


# @pytest.mark.parametrize('given, expected',
#                         [(('andrew', 'pass', False), ('andrew', 'pass', False)),
#                          (('man', 'strong_pass', False), ('man', 'strong_pass', False))
#                         ]
#                         )
# def test_user_init(given, expected):
#     user = project.models.User(*given)
#     assert user.username == given[0]
#     assert user.password == generate_password_hash(given[1])
#     assert user.is_admin == given[2]
#     assert user.created != datetime.datetime.utcnow()
