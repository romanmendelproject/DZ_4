from base_connect import Session, Base, engine
from models import Post, Tag, User
import json


def create_data():
    with open('src\\data\\data.json', 'r', encoding='utf-8') as f:
        json_dict = json.load(f)

    Base.metadata.create_all(engine)
    session = Session()

    for tags in json_dict["tags"]:
        tag = Tag(name=tags["tag"])
        session.add(tag)

    for users in json_dict["users"]:
        print(users["login"])
        user = User(username=users["login"], firstname=users["firstname"], lastname=users["lastname"])
        session.add(user)
        session.flush()
        for posts in users["posts"]:
            post = Post(user_id=user.id, title=posts["title"], text=posts["text"])
            session.add(post)
            for tags in posts["tags"]:
                tag = session.query(Tag).filter(Tag.name == tags["tag"]).all()
                post.tags.extend(tag)
    session.commit()
