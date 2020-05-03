from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Article, ArticleType,Tags

def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),username=fake.user_name(), password='password',confirmed=True,first_name=fake.name(),about_me=fake.text(),member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i +=1
        except IntegrityError:
            db.session.rollback()

def articles(count=100):
    fake = Faker()
    user_count = User.query.count()
    type_count = ArticleType.query.count()
    types = ArticleType.query.all()
    for i in range(count):
        u = User.query.offset(randint(0,user_count - 1)).first()
        a = Article(title=fake.sentence(nb_words=4),
            body= '\n\n'.join(fake.paragraphs(nb=3)),
            blurb=fake.text(),
            publish_date=fake.past_date(),
            author=u,
            image="https://www.eskimotv.net/img/site-resource/logo-page.jpg",
            type=types[randint(0,type_count - 1)])
        db.session.add(a)
    db.session.commit()

def tag_articles():
    article_count = Article.query.count()
    tag_count = Tags.query.count()
    for article in Article.query.all():
        if article.id > 10:
            continue
        for tags_to_add in range(0,randint(4,10)):
            for attempt in range(10):
                new_tag = Tags.query.get(randint(1,tag_count))
                if new_tag not in article.tags.all():
                    article.tags.append(new_tag)
                    break
        db.session.add(article)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            exit()
