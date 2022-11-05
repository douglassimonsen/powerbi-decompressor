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
  page_id int references pbi.pages(id),

  height float,
  width float,
  x float,
  y float,
  z float
);
create table pbi.data_sources (
  id serial primary key not null,
  report_id int references pbi.reports(id),
  source_type text,
  source_details jsonb,
  pbi_id text,
  name text
);
create table pbi.data_source_columns (
  id serial primary key not null,
  data_source_id int references pbi.data_sources(id),
  name text,
  data_type text
);