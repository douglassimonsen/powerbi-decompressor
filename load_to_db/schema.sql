drop schema if exists pbi cascade;
create schema pbi;

create table pbi.reports (
  id serial primary key not null,
  file_path text,
  name text GENERATED ALWAYS AS (split_part(
	  file_path, '/', 
	  array_length(string_to_array(file_path, '/'), 1)
  )) stored,
  pbi_id text,
  layoutOptimization int,
  theme text,
  layout jsonb,
  created_dt timestamp
);
create table pbi.pages (
  id serial primary key not null,
  report_id int references pbi.reports(id),
  name text,
  ordinal int,
  config jsonb,
  displayOption int,
  width float,
  height float,
  raw jsonb
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
  z float,
  filter_on_drill boolean,
  raw jsonb
);
create table pbi.datasources (
  id serial primary key not null,
  name text, 
  pbi_id text, 
  report_id int, 
  tableId int,
  source_type text, 
  source_details jsonb,
  QueryDefinition text,
  raw jsonb
);
create table pbi.tables (
  id serial primary key not null,
  pbi_id text,
  datasourceID int references pbi.datasources(id),
  report_id int references pbi.reports(id),
  source_type text,
  source_details jsonb,
  name text,
  raw jsonb
);
create table pbi.datatypes (
  id serial primary key not null,
  pbi_id text,
  Name text,
  raw jsonb
);
create table pbi.measures (
  id serial primary key not null,
  pbi_id text,
  TableID int references pbi.tables(id),
  name text,
  Expression text,
  data_type int references pbi.datatypes(id),
  raw jsonb
);
create table pbi.columns (
  id serial primary key not null,
  pbi_id text,
  TableID int references pbi.tables(id),
  name text,
  data_type int references pbi.datatypes(id),
  isHidden boolean,
  expression text,
  raw jsonb
);
create table pbi.dax_dependencies (
  id serial primary key not null,
  child_id int, -- can't specify a foreign key because it could be two separate tables
  child_pbi_id text, 
  child_type text, 
  parent_id int, -- can't specify a foreign key because it could be two separate tables
  parent_pbi_id text, 
  parent_type text,
  dependency_type text
);
