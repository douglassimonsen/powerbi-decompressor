insert into pbi.datasources (name, pbi_id, report_id, QueryDefinition, source_type, source_details)
values (%(name)s, %(pbi_id)s, %(report_id)s, %(QueryDefinition)s, %(source_type)s, %(source_details)s)
returning pbi_id, id;