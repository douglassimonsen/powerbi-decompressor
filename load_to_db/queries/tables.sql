insert into pbi.tables (name, pbi_id, datasourceID, report_id)
values (%(name)s, %(pbi_id)s, %(datasourceID)s, %(report_id)s)
returning pbi_id, id;