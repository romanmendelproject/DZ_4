from sqlalchemy import create_engine, \
    Table, Column, ForeignKey, Boolean, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import func

Base = declarative_base()
engine = create_engine('sqlite:///blog.db')

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


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


def create_data():
    """Наполняем базу данными"""

    Base.metadata.create_all(engine)
    session = Session()

    user = User(username='mendel', firstname="Ivan", lastname="Ivanov")
    user2 = User(username='mendel2', firstname="Ivan2", lastname="Ivanov2")
    session.add(user)
    session.add(user2)
    session.flush()

    post1 = Post(user_id=user.id, title='Жим лежа', text='Базовое упражнение в бодибилдинге и пауэрлифтинге со свободными весами,\
    предназначенное для развития мышц груди, рук (трицепсов) и переднего пучка дельтовидных мышц. ')
    post2 = Post(user_id=user.id, title='Становая тяга', text='Базовое (многосуставное) упражнение, выполняемое обычно со штангой,\
    а также с гантелью или гирей, удерживаемыми между ног обеими руками.')
    post3 = Post(user_id=user.id, title='Приседания', text='Одно из базовых силовых упражнений (в том числе в пауэрлифтинге и культуризме);\
    выполняющий упражнение приседает и затем встаёт, возвращаясь в положение стоя.')
    post4 = Post(user_id=user.id, title='Сведение рук', text='Физическое упражнение, изолированно нагружающее большие грудные мышцы,\
    основная функция которых состоит как раз в сведении рук.')
    post5 = Post(user_id=user2.id, title='Тест', text='Тест')

    tag1 = Tag(name='штанга')
    tag2 = Tag(name='гантели')
    tag3 = Tag(name='гири')
    post1.tags.append(tag1)
    post1.tags.append(tag2)
    post2.tags.append(tag1)
    post2.tags.append(tag2)
    post3.tags.append(tag1)
    post3.tags.append(tag2)
    post3.tags.append(tag3)
    post4.tags.append(tag2)
    post5.tags.append(tag1)
    session.add(post1)
    session.add(post2)
    session.add(post3)
    session.add(post4)
    session.add(post5)
    session.add(tag1)
    session.add(tag2)
    session.add(tag3)
    session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    #create_data() Выполнять при первом запуске, чтобы наполнить данными таблицы.
    session = Session()
    AMOUNT_TAG = 2
    """Вариант 1 с выводом нужных тегов"""

    """Делаем запрос со счетчиком тегов, а также указываем нужного пользователя"""
    q = session.query(tags_posts_table.c.post_id, func.count(tags_posts_table.c.post_id))\
        .join(Post).join(User)\
        .filter(User.username == 'mendel')\
        .group_by(tags_posts_table.c.post_id).all()
    print("\n")
    """Делаем запрос всех постов, у которых количество тегов равно 2"""
    for q_item in q:
        if q_item[1] == AMOUNT_TAG:
            qry_doble_post = session.query(Post, Tag, User).join(User)\
                .join(tags_posts_table).join(Tag)\
                .filter(Post.id == q_item[0]).all()
            print(f"Пользователь: {qry_doble_post[0].User.username}")
            print(f"Пост: {qry_doble_post[0].Post.title}\nТеги:", end=" ")
            for qry_doble_post_item in qry_doble_post:
                print(qry_doble_post_item.Tag.name, end=" ")
            print("\n")

    """Вариант 2 только посты"""

    qry_doble_only_post = session.query(Post)\
        .join(User).join(tags_posts_table)\
        .join(Tag).filter(User.username == 'mendel')\
        .group_by(Post.id).having(func.count(Tag.id) == AMOUNT_TAG)\
        .all()

    print(qry_doble_only_post)