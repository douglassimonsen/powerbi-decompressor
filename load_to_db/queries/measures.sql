insert into pbi.measures (name, pbi_id, TableID, Expression)
values (%(name)s, %(pbi_id)s, %(TableID)s, %(Expression)s)
returning pbi_id, id;