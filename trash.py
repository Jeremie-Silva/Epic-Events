class AbstractBaseModel:
    __abstract__ = True

    # @classmethod
    # def create(cls, **kwargs):
    #     if "phone" in kwargs:
    #         cls.is_valid_phone_number(kwargs["phone"])
    #     if "password" in kwargs:
    #         kwargs["password"] = bcrypt.hash(kwargs["password"])
    #     if "email" in kwargs:
    #         cls.is_valid_email(kwargs["email"])
    #     return cls(**kwargs)
    #
    # @classmethod
    # def is_valid_phone_number(cls, phone: str):
    #     if not is_valid_number(parse(phone)):
    #         raise InvalidData("Invalid phone number")
    #
    # @classmethod
    # def is_valid_email(cls, email: str):
    #     if not validate_email(email):
    #         raise InvalidData("Invalid email")
    #
    # @classmethod
    # def get_item(cls, **conditions) -> object | None:
    #     session: Session = SessionLocal()
    #     accumulated_query = session.query(cls)
    #     for field, value in conditions.items():
    #         accumulated_query = accumulated_query.filter(getattr(cls, field) == value)
    #     return accumulated_query.first()
    #
    # @classmethod
    # def get_list(cls) -> list[object]:
    #     session: Session = SessionLocal()
    #     return session.query(cls).all()

class InvalidData(Exception):
    pass
