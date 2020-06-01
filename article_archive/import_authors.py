from frontmatter import Frontmatter
authors = Frontmatter.read_file('article_archive/authors.yml')['attributes']
role = Role.query.filter_by(name="Writer").first()
for author in authors:
    print(author)
    if not User.query.filter_by(username=author).first():
        u = User(username=author,first_name=authors[author]['name'].split(' ')[0],last_name=authors[author]['name'].split()[1],email=authors[author]['email'],role=role,about_me=authors[author].get('bio'))
        db.session.add(u)
        db.session.commit()
