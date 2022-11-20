insert into pbi.reports (file_path, created_dt)
values (%(file_path)s, %(created_dt)s)
returning id;