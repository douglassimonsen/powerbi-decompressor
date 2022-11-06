insert into pbi.reports (name)
values (%(name)s)
returning id;