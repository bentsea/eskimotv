import glob
import json
import html
import os
from frontmatter import Frontmatter
from datetime import datetime
from markdown import markdown
from slugify import slugify
from PIL import Image
from app.admin import files
from app.admin.views import add_new_creative_work

image_path = 'article_archive'

with open('article_archive/all_content.json') as json_file:
    all_content = json.loads(json_file.read().replace('\n','\\n').replace('\t',' ')[:-2])

articles = glob.glob('article_archive/_posts/**/*.markdown', recursive=True)
for article_path in articles:
    article = Frontmatter.read_file(article_path)
    article_object = Article.query.filter_by(title_slug=slugify(article['attributes']['title'])).first()
    if not article_object:
        article_object = Article(title=article['attributes']['title'])
    else:
        suffixes={0:" Alternate",1:" II",2:"I"}
        title_try_i = 0
        while Article.query.filter_by(title_slug=slugify(article['attributes']['title'])).first():
            article['attributes']['title']=f"{article['attributes']['title']}{suffixes[title_try_i]}"
            title_try_i += 1
        article_object = Article(title=slugify(article['attributes']['title']))
    cover_img = Image.open(f"{image_path}{article['attributes']['image']}")
    if article['attributes'].get('subjectInfo'):
        same_as= article['attributes']['subjectInfo']['about']['sameAs']
        if same_as.find('imdb.com') != -1:
            creative_work = add_new_creative_work(imdb_id=same_as.split('/')[-1])
        elif same_as.find('themoviedb.org') != -1:
            creative_work = add_new_creative_work(tmdb_id=same_as.split('/')[-1],media_type=same_as.split('/')[-2])
        else:
            continue
    article_object.subject = creative_work
    article_object.body = html.unescape(all_content[article_path.replace('article_archive/','')])
    article_object.blurb = article['attributes'].get('blurb','The author of this article was lazy and forgot to write a blurb.')
    if article['attributes'].get('reviewInfo'):
        article_object.rating = article['attributes']['reviewInfo']['rating']
        article_object.final_verdict = article['attributes']['reviewInfo']['final-verdict']
    article_object.author = User.query.filter_by(username=article['attributes']['author']).first()
    article_object.type = ArticleType.query.filter_by(name=article['attributes']['categories'][0].title()).first()
    for category in article['attributes']['categories'][2:]:
        tag = Tags.query.filter_by(name=category.title()).first()
        if not tag:
            tag = Tags(name=category.title())
            db.session.add(tag)
            db.session.commit()
        if tag not in article_object.tags.all():
            article_object.tags.append(tag)
    if article['attributes'].get('youtube'):
        article_object.youtube = article['attributes']['youtube']
    if article['attributes'].get('published'):
        article_object.is_published = article['attributes'].get('published')
    else:
        article_object.is_published = True
    article_object.publish_date = datetime.strptime(article_path.split('/')[-1][:10],'%Y-%m-%d')
    article_object.image = files.save_cover_image(cover_img,article_object.title_slug)
    try:
        db.session.add(article_object)
        db.session.commit()
    except Exception as err:
        print(err)
        db.session.rollback()
