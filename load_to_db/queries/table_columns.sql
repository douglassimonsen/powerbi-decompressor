insert into pbi.table_columns (pbi_id, name, Table_id, data_type, isHidden, Expression)
values (%(pbi_id)s, %(name)s, %(table_id)s, %(data_type)s, %(isHidden)s, %(Expression)s)
returning pbi_id, id;