with get_count_per_room
as
(

select 
	rooms, 
	count(*) as cnt
from 
	datamart.offerts
where formatted_date = '2024-10'
group by rooms
)
select 
	rooms, 
	cnt,
	SUM(cnt) OVER () AS total_cnt,
	ROUND(cnt / SUM(cnt) OVER (), 3) as percentage
from 
get_count_per_room
order by percentage desc