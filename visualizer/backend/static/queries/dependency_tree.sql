with recursive parents as (
	select dd.* from pbi.dax_dependencies dd
	where id = 278
	union all
	select dd2.* from pbi.dax_dependencies dd2 
	inner join parents b 
	on dd2.parent_id = b.child_id
	and dd2.parent_type = b.child_type
), children as (
	select dd.* from pbi.dax_dependencies dd
	where id = 278
	union all
	select dd2.* from pbi.dax_dependencies dd2 
	inner join children b 
	on dd2.child_id = b.parent_id
	and dd2.child_type = b.parent_type
)
select * from parents
union
select * from children