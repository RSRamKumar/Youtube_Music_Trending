
-- Display all the records
SELECT * FROM "AwsDataCatalog"."youtube_data_crawler_db"."youtube_data_bucket_ram" limit 5;

-- Show the longest song_title 
SELECT song_title, duration_in_seconds from "AwsDataCatalog"."youtube_data_crawler_db"."youtube_data_bucket_ram"
where duration_in_seconds = (
SELECT max(duration_in_seconds) FROM "AwsDataCatalog"."youtube_data_crawler_db"."youtube_data_bucket_ram"
);
 
-- Show average views_count across the channels
SELECT channel, 
avg(views_count) as AverageViews 
FROM "AwsDataCatalog"."youtube_data_crawler_db"."youtube_data_bucket_ram"
group by channel order by AverageViews desc limit 5;

-- Show the count of videos for each language
SELECT language, count(language) as count
from "AwsDataCatalog"."youtube_data_crawler_db"."youtube_data_bucket_ram"
group by language
order by count desc;

-- Show average views_count across the language
SELECT language, avg(views_count) as avg_view_count
from  "AwsDataCatalog"."youtube_data_crawler_db"."youtube_data_bucket_ram"
group by language
order by avg_view_count;  

-- Show song_title with highest views 
select song_title from "AwsDataCatalog"."youtube_data_crawler_db"."youtube_data_bucket_ram"
where views_count = (
select max(views_count) from 
"AwsDataCatalog"."youtube_data_crawler_db"."youtube_data_bucket_ram"
);

-- Show song_title with highest views again
select song_title, views_count
from  "AwsDataCatalog"."youtube_data_crawler_db"."youtube_data_bucket_ram"
order by views_count desc limit 1;  
 
