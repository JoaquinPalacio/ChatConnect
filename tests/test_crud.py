import pytest
from sqlmodel import Session, SQLModel, create_engine
from crud.users import get_user_by_username, create_user
from crud.rooms import create_room, get_room_by_id, get_room_id_by_name


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


def test_create_user_duplicate(session):
    create_user(session, "testuserdup", "testpass")
    with pytest.raises(Exception):
        create_user(session, "testuserdup", "testpass2")


def test_get_nonexistent_user(session):
    fetched = get_user_by_username(session, "nonexistent")
    assert fetched is None


def test_create_and_get_room(session):
    room = create_room(session, "Test Room", owner_id=None, is_private=False)
    assert room.id is not None, "Room ID should not be None"
    fetched = get_room_by_id(session, room.id)
    assert fetched is not None
    assert fetched.id == room.id
    assert fetched.name == "Test Room"


def test_get_room_by_name(session):
    room = create_room(session, "Unique Room", owner_id=None, is_private=False)
    room_id = get_room_id_by_name(session, "Unique Room")
    assert room_id == room.id


def test_get_nonexistent_room(session):
    fetched = get_room_by_id(session, 999)
    assert fetched is None


def test_create_room_duplicate_name(session):
    create_room(session, "Duplicate Room", owner_id=None, is_private=False)
    with pytest.raises(Exception):
        create_room(session, "Duplicate Room", owner_id=None, is_private=False)
