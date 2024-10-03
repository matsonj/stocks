select
    "filename" as "file",
    regexp_extract("filename", 'data/(.+?)_\d+\.csv', 1) as entity,
    last_modified as modified_ts
from read_blob('data/*.csv')