drop schema if exists pbi cascade;
create schema pbi;

create table pbi.reports (
  id serial primary key not null,
  name text
);
create table pbi.pages (
  id serial primary key not null,
  report_id int references pbi.reports(id),
  name text,
  ordinal int,
  filter_id int,  -- TODO
  config jsonb,
  displayOption int,
  width float,
  height float
);
create table pbi.visuals (
  id serial primary key not null,
  pbi_id text,
  page_id int references pbi.pages(id),
  visual_type text,
  height float,
  width float,
  x float,
  y float,
  z float
);
create table pbi.tables (
  id serial primary key not null,
  pbi_id int,
  report_id int references pbi.reports(id),
  source_type text,
  source_details jsonb,
  name text
);
create table pbi.table_columns (
  id serial primary key not null,
  pbi_id int,
  table_id int references pbi.tables(id),
  name text,
  data_type text,
  isHidden boolean
);
create table pbi.visual_table_columns (
  id serial primary key not null,
  visual_id int references pbi.visuals(id),
  table_column_id int references pbi.table_columns(id),
  visual_use text
);