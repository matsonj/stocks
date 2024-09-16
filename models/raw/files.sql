select "file", regexp_extract("file", 'data/(.+?)_\d+\.csv', 1) as entity
from glob('data/*.csv')
