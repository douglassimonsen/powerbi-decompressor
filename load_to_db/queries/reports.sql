insert into pbi.reports (file_path)
values (%(file_path)s)
returning id;