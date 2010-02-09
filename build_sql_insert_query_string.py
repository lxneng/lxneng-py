# SQL fields
l = []
l.append(['section', 'art_gallery'])
l.append(['category', 'just a test'])
l.append(['type', 'image'])
 
# build SQL query
keys = [e[0] for e in l]
values = [e[1] for e in l]
values = [e.replace("'", "''") for e in values]
query = """insert into `media` (`%s`) values ('%s');""" % ("`, `".join(keys), "', '".join(values), )
 
print query
