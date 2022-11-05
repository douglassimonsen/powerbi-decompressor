insert into pbi.datasource_columns (pbi_id, name, datasource_id, data_type, isHidden)
values (%(pbi_id)s, %(name)s, %(datasource_id)s, %(data_type)s, %(isHidden)s)
returning pbi_id, id;