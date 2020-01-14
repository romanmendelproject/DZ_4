from sqlalchemy import Table, Column, ForeignKey, Boolean, Integer, String, Text
from sqlalchemy.orm import relationship
from base_connect import Base

tags_posts_table = Table(
    'tags_posts',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(16), nullable=False)
    text = Column(Text, nullable=False)
    is_publised = Column(Boolean, nullable=False, default=False)
    user = relationship("User", back_populates="posts", lazy="joined")
    tags = relationship("Tag", secondary=tags_posts_table, back_populates="posts")

    def __repr__(self):
        return f'<Post #{self.id} {self.title}>'


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    posts = relationship("Post", secondary=tags_posts_table, back_populates="tags")

    def __repr__(self):
        return f'<Tag #{self.id} {self.name}>'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(10), nullable=False)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(30), nullable=False)
    posts = relationship("Post", back_populates="user")

    def __repr__(self):
        return f'<User #{self.id} {self.username}>'
