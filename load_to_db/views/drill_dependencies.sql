create materialized view pbi.drill_dependencies as (
	with recursive column_drill_dependencies as (
		select r.from_column_id, r.to_column_id  
		from pbi.relationships r 
		where r.is_active = true
		union 
		select r2.to_column_id as from_column_id, r2.from_column_id as to_column_id 
		from pbi.relationships r2
		where r2.is_active = true
		and r2.cross_filtering_behavior = 2
	), table_drill_dependencies as (
		select from_c.table_id as from_table_id,  to_c.table_id as to_table_id from column_drill_dependencies c
		left join pbi.columns from_c
		on c.from_column_id = from_c.id
		left join pbi.columns to_c
		on c.to_column_id = to_c.id
	), all_table_dependencies as (
		select *
		from table_drill_dependencies tdd
		union
		select atd.from_table_id, tdd.to_table_id
		from table_drill_dependencies tdd
		inner join all_table_dependencies atd
		on tdd.from_table_id = atd.to_table_id
		where atd.from_table_id <> tdd.to_table_id
	), visual_drill_info as (
		select rp.child_id, c.table_id, v.page_id, v.drill_filter_other_visuals 
		from pbi.root_parents rp 
		left join pbi.columns c
		on rp.root_id = c.id
		left join pbi.visuals v 
		on rp.child_id  = v.id
		where rp.child_type = 'visual'
		and rp.root_type  = 'column'
	), drill_impacted_tables as (
		select vdi.*,
		       atd.to_table_id      
		from visual_drill_info vdi
		inner join all_table_dependencies atd
		on vdi.table_id = atd.from_table_id
	), drill_impacts as (
		select distinct dit.child_id as from_visual,
		       dit2.child_id as to_visual
		from drill_impacted_tables dit
		inner join drill_impacted_tables dit2
		on (
			dit.table_id = dit2.table_id or
			dit.to_table_id = dit2.table_id
		)
		and dit.page_id = dit2.page_id
		where dit.drill_filter_other_visuals = true
		and dit.child_id <> dit2.child_id
	)
	select * from drill_impacts
)