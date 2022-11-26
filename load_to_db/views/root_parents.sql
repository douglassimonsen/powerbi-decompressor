
create view pbi.root_parents as (
	with recursive children as (
		select dd.parent_id as root_id, 
		       dd.parent_type  as root_type, 
		       dd.child_id,
		       dd.child_type 
		from pbi.dax_dependencies dd
	
		union all
	
		select b.root_id,
		       b.root_type,
		       dd2.child_id,
		       dd2.child_type 
		from pbi.dax_dependencies dd2 
		inner join children b 
		on dd2.parent_id  = b.child_id
		and dd2.parent_type  = b.child_type
	)
	select * from children
)