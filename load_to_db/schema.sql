drop schema if exists pbi cascade;
create schema pbi;

create table pbi.reports (
  id serial primary key not null,
  file_path text,
  name text GENERATED ALWAYS AS (split_part(
	  file_path, '/', 
	  array_length(string_to_array(file_path, '/'), 1)
  )) stored
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
create table pbi.datasources (
  id serial primary key not null,
  name text, 
  pbi_id text, 
  report_id int, 
  source_type text, 
  source_details jsonb,
  QueryDefinition text
);
create table pbi.tables (
  id serial primary key not null,
  pbi_id text,
  datasourceID int references pbi.datasources(id),
  source_type text,
  source_details jsonb,
  name text
);
create table pbi.measures (
  id serial primary key not null,
  pbi_id text,
  TableID int references pbi.tables(id),
  name text,
  Expression text
);
create table pbi.table_columns (
  id serial primary key not null,
  pbi_id text,
  table_id int references pbi.tables(id),
  name text,
  data_type text,
  isHidden boolean,
  expression text
);
create table pbi.dax_dependencies (
  id serial primary key not null,
  child_id int, -- can't specify a foreign key because it could be two separate tables
  child_pbi_id text, 
  child_type text, 
  parent_id int, -- can't specify a foreign key because it could be two separate tables
  parent_pbi_id text, 
  parent_type text
);
