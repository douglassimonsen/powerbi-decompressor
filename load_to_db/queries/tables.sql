insert into pbi.tables (name, pbi_id, datasourceID)
values (%(name)s, %(pbi_id)s, %(datasourceID)s)
returning pbi_id, id;