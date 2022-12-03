with base as (
	select v.id as child_id, 'visual' as child_type
	from pbi.visuals v
	inner join pbi.pages p 
	on v.page_id = p.id
	where p.report_id = %(id)s
	union all
	select m.id as child_id, 'measure' as child_type
	from pbi.measures m  
	inner join pbi."tables" t 
	on m.tableid = t.id
	where t.report_id = %(id)s
	union all
	select tc.id as child_id, 'visual' as child_type
	from pbi.columns tc
	inner join pbi."tables" t 
	on tc.tableid = t.id
	where tc."expression" is not null
	and t.report_id = %(id)s
)
select dd.* from base
inner join pbi.dax_dependencies dd 
on base.child_id = dd.child_id
and base.child_type = dd.child_type
