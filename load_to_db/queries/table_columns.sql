insert into pbi.table_columns (pbi_id, name, TableID, data_type, isHidden, Expression)
values (%(pbi_id)s, %(name)s, %(TableID)s, %(data_type)s, %(isHidden)s, %(Expression)s)
returning pbi_id, id;