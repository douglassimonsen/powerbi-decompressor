select v.*, p.*
from pbi.visuals v 
left join pbi.pages p 
on v.page_id = p.id 
where p.report_id = 1