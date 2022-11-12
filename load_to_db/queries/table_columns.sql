insert into pbi.table_columns (pbi_id, name, table_id, data_type, isHidden)
values (%(pbi_id)s, %(name)s, %(table_id)s, %(data_type)s, %(isHidden)s)
returning pbi_id, id;