drop schema if exists pbi cascade;
create schema pbi;

create table pbi.reports (
  id serial primary key not null,
  name text
);
create table pbi.pages (
  id serial primary key not null,
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
  page_id int reference pbi.pages(id),
  
  height float,
  width float,
  x float,
  y float,
  z float
)