insert into pbi.pages (name, ordinal, report_id)
values (%(name)s, %(ordinal)s, %(report_id)s)
returning ordinal, id;