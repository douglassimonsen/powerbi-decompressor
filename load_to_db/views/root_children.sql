
create view pbi.root_children as (
	with recursive parents as (
		select dd.child_id as root_id, 
		       dd.child_type  as root_type, 
		       dd.parent_id,
		       dd.parent_type 
		from pbi.dax_dependencies dd
	
		union all
	
		select b.root_id,
		       b.root_type,
		       dd2.parent_id,
		       dd2.parent_type 
		from pbi.dax_dependencies dd2 
		inner join parents b 
		on dd2.child_id  = b.parent_id
		and dd2.child_type  = b.parent_type
	)
	select * from parents
)