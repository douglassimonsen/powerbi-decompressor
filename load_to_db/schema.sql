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
  layout_optimization int,
  theme text,
  culture text,
  layout jsonb,
  modified_time timestamp,
  raw jsonb
);
create table pbi.pages (
  id serial primary key not null,
  report_id int references pbi.reports(id),
  name text,
  ordinal int,
  config jsonb,
  display_option int,
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
  drill_filter_other_visuals boolean,
  raw jsonb
);
create table pbi.data_sources (
  id serial primary key not null,
  name text,
  pbi_id text,
  report_id int references pbi.reports(id), 
  type int,
  max_connections int,
  modified_time timestamp,
  connection_string text,
  impersonation_mode int,
  timeout int,
  raw jsonb
);
create table pbi.expressions (
  id serial primary key not null,
  name text,
  pbi_id text,
  report_id int references pbi.reports(id),
  kind int,
  expression text,
  modified_time timestamp,
  raw jsonb
);
create table pbi.linguistic_metadata (
  id serial primary key not null,
  pbi_id text,
  culture_id int,
  language text,
  dynamic_improvement text,
  entities jsonb,
  relationships jsonb,
  examples jsonb,
  report_id int references pbi.reports(id),
  version text,
  modified_time timestamp
);
create table pbi.annotation_object_types (
  id serial primary key not null,
  pbi_id text,
  name text
);
create table pbi.annotations (
  id serial primary key not null,
  pbi_id text,
  report_id int references pbi.reports(id),
  object_type int references pbi.annotation_object_types(id),
  object_id text,
  name text,
  value text,
  modified_time timestamp
);
create table pbi.tables (
  id serial primary key not null,
  pbi_id text,
  report_id int references pbi.reports(id),
  name text,
  raw jsonb
);
create table pbi.partitions (
  id serial primary key not null,
  name text, 
  pbi_id text, 
  table_id int references pbi.tables(id),
  data_source_id int references pbi.data_sources(id),
  source_type text, 
  source_details jsonb,
  query_definition text,
  raw jsonb
);
create table pbi.datatypes (
  id serial primary key not null,
  pbi_id text,
  name text,
  raw jsonb
);
create table pbi.measures (
  id serial primary key not null,
  pbi_id text,
  table_id int references pbi.tables(id),
  name text,
  expression text,
  data_type int references pbi.datatypes(id),
  raw jsonb
);
create table pbi.hierarchies (
  id serial primary key not null,
  pbi_id text,
  name text,
  is_hidden boolean,
  modified_time timestamp,
  structure_modified_time timestamp,
  refreshed_time timestamp,
  hide_members int,
  state int,
  table_id int references pbi.tables(id)
);
create table pbi.columns (
  id serial primary key not null,
  pbi_id text,
  table_id int references pbi.tables(id),
  name text,
  data_type int references pbi.datatypes(id),
  is_hidden boolean,
  expression text,
  raw jsonb
);
create table pbi.levels (
  id serial primary key not null,
  pbi_id text,
  hierarchy_id int references pbi.hierarchies(id),
  ordinal int,
  name text,
  column_id int references pbi.columns(id),
  hierarchy_column_id int references pbi.columns(id),
  modified_time timestamp 
);
create table pbi.relationship_crossfilter_types (
  id serial primary key not null,
  pbi_id text,
  name text
);
create table pbi.relationship_cardinalities (
  id serial primary key not null,
  pbi_id text,
  name text
);
create table pbi.relationships (
  id serial primary key not null,
  from_column_id int references pbi.columns(id),
  from_cardinality int references pbi.relationship_cardinalities(id),
  to_column_id int references pbi.columns(id),
  to_cardinality int references pbi.relationship_cardinalities(id),
  cross_filtering_behavior int references pbi.relationship_crossfilter_types(id),
  is_active boolean,
  pbi_id text,
  name text,
  modified_time timestamp,
  refreshed_time timestamp,
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
