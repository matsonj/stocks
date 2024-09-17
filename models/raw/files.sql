select
    "file",
    regexp_extract("file", 'data/(.+?)_\d+\.csv', 1) as entity,
    -- Extract the timestamp part and format it using strptime
    strptime(regexp_extract("file", '_(\d+)\.csv', 1), '%Y%m%d%H%M%S') as timestamp
from glob('data/*.csv')
