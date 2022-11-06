insert into pbi.visuals (pbi_id, visual_type, height, width, x, y, z, page_id)
values (%(pbi_id)s, %(visual_type)s, %(height)s, %(width)s, %(x)s, %(y)s, %(z)s, %(page_id)s)
returning pbi_id, id;