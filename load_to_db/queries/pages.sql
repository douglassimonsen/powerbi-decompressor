insert into pbi.pages (name, ordinal, report_id, height, width)
values (%(name)s, %(ordinal)s, %(report_id)s, %(height)s, %(width)s)
returning ordinal, id;