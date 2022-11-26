create or replace view pbi.measures_depedency_counts as (
	with base as (
		select c.root_id,
		       c.root_type,
		       sum(case when c.child_type = 'visual' then 1 else 0 end) as dependent_visuals,
		       sum(case when c.child_type = 'measure' then 1 else 0 end) as dependent_measures,
		       sum(case when c.child_type = 'column' then 1 else 0 end) as dependent_columns -- remember the 
		from pbi.root_parents c
		group by c.root_id,
		         c.root_type
	)
	select r."name" as report, 
	       t."name" as "table", 
	       m."name" as "measure", 
	       COALESCE(b.dependent_visuals, 0) as dependent_visuals, 
	       COALESCE(b.dependent_measures, 0) as dependent_measures,  
	       COALESCE(b.dependent_columns, 0) as dependent_columns
	from pbi.measures m 
	left join pbi."tables" t 
	on m.tableid = t.id
	left join pbi.reports r 
	on t.report_id = r.id
	left join base b
	on m.id = b.root_id
	and b.root_type = 'measure'
)

