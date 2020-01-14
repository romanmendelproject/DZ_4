from base_connect import Session, Base, engine
from models import Post, Tag, User, tags_posts_table
from sqlalchemy import func
from data_base import create_data


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    create_data() #Выполнять при первом запуске, чтобы наполнить данными таблицы.
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