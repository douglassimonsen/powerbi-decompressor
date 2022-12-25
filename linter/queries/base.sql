select v.*, 
       p.id as page_id, 
       p.width as page_width, 
       p.height page_height
from pbi.visuals v 
left join pbi.pages p 
on v.page_id = p.id 
where p.report_id = 1