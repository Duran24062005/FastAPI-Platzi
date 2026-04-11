from sqlalchemy.orm import Session

from app.model.user_model import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user_data: dict) -> User:
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all(self) -> list[User]:
        return self.db.query(User).all()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def rollback(self) -> None:
        self.db.rollback()
