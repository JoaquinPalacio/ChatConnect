import pytest
from sqlmodel import Session, SQLModel, create_engine
from crud.users import get_user_by_username
from crud.user import create_user


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_and_get_user(session):
    user = create_user(session, "testuser", "testpass")
    fetched = get_user_by_username(session, "testuser")
    assert fetched is not None
    assert fetched.id == user.id
    assert fetched.username == "testuser"
