import uuid

from dbmodels import User
from exception.not_found_exception import NotFoundException
from query2dict import queryToDict
from RSA import rsaDecrypt, privkey

class UserCRUD:
    def __init__(self, db):
        self.db = db

    async def create_user(self, userid, name=None,  gender=None, role=None, password=None):
        # id = str(uuid.uuid4())
        user1 = User(userid=userid, name=name, gender=gender, role=role, password=password)
        self.db.add(user1)
        self.db.commit()
        return id

    async def login_verify(self, id: str, password):
        """
        查询姓名
        :param id:
        :return:
        """
        user = self.db.query(User).filter(
            User.userid == id
        ).first()

        print(rsaDecrypt(user.password, privkey))
        print(rsaDecrypt(password, privkey))
        if not user:
            return False
        else:
            if rsaDecrypt(user.password, privkey) != rsaDecrypt(password, privkey):
            # if user.password != password:
                status = False
            else:
                status = True
            if user.role == 0:
                isStudent = True
            else:
                isStudent = False
            return {'status': status, 'isStudent': isStudent}

    async def get_tea(self):
        return queryToDict(self.db.query(User.userid, User.name).filter(User.role == 1).all())


    async def get_user(self):
        return queryToDict(self.db.query(User.userid, User.name, User.role, User.gender).filter().all())


    async def get_name(self):
        return queryToDict(self.db.query(User.userid, User.name).filter().all())
