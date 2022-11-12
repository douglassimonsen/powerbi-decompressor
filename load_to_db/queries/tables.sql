insert into pbi.tables (name, pbi_id, report_id, source_type, source_details)
values (%(name)s, %(pbi_id)s, %(report_id)s, %(source_type)s, %(source_details)s)
returning pbi_id, id;