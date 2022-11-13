select v.*,
       r.id as report_id,
       p.id as page_id,
       p.ordinal,
       p.name as page_name,
       p.width as page_width,
       p.height as page_height
from pbi.reports r
left join pbi.pages p 
on p.report_id = r.id
left join pbi.visuals v 
on v.page_id = p.id
where r.id = {id}
