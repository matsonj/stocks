select
    "file",
    regexp_extract("file", 'data/(.+?)_\d+\.csv', 1) as entity,
    strptime(regexp_extract("file", '_(\d+)\.csv', 1), '%Y%m%d%H%M%S') as timestamp
from glob('data/*.csv')
