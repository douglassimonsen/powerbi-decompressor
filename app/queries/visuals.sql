insert into pbi.visuals (pbi_id, height, width, x, y, z, page_id)
values (%(pbi_id)s, %(height)s, %(width)s, %(x)s, %(y)s, %(z)s, %(page_id)s)
returning pbi_id, id;