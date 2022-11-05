insert into pbi.datasources (name, pbi_id)
values (%(name)s, %(pbi_id)s)
returning pbi_id, id;