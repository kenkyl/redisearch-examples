# redisearch-examples
## Overview
Some basic Python examples of using the [RediSearch](https://oss.redislabs.com/redisearch/) module to create an index, add documents (stored as Redis Hash objects), and query those documents.
RediSearch automatically creates and manages the multiple, complex indexes needed to query the documents stored. 

## Basic Process
1. [FT.CREATE](https://oss.redislabs.com/redisearch/Commands/#ftcreate) --> create a new index 
- *redis-cli* example: `FT.CREATE session_index SCHEMA app_oid TAG NOINDEX vnf_id TAG thread_id TAG timestamp NUMERIC SORTABLE ktab TAG`

2. [FT.ADD](https://oss.redislabs.com/redisearch/Commands/#ftadd) --> add documents to the index
- *redis-cli* example: `FT.ADD session_index session:<id> app_oid 9999 vnf_id 1234 thread_id 1 timestamp 1595004682 ktab 4321`

3. [FT.SEARCH](https://oss.redislabs.com/redisearch/Commands/#ftsearch) / [FT.AGGREGATE](https://oss.redislabs.com/redisearch/Commands/#ftaggregate) --> run queries against the index
- *redis-cli* example: `FT.SEARCH session_index @ktab:{4321} @vnf_id:{1234} @thread_id:{1} @timestamp:[1595004682 +inf] SORTBY timestamp ASC`

## Notes
- It is recommended to use the [Quick Start](https://oss.redislabs.com/redisearch/Quick_Start/) guide and launch a RediSearch Docker container for quick testing. You can also easily load the RediSearch module into an exisitng or new [Redis Enterprise](https://redislabs.com/try-free/) database 
- The Python RediSearch library, [redisearch-py](http://github.com/RedisLabs/redisearch-py), is imported separately from the standard [redis-py](https://github.com/andymccurdy/redis-py) library
- Small random numbers are used for each of the document fields for simplicity's sake 
- This script does **not** clear the keys in the redis database. To inspect the indexes and session documents created, run the KEYS command in the *redis-cli*. To clear out the database, run the FLUSHALL command in the *redis-cli* (don't run either of these commands in production!)
- The more times you run the script without clearing the database, the more documents should be returned by the first two query examples
- For complex queries, create an instance of the [Query](https://oss.redislabs.com/redisearch/python_client/#class_query) object, as in the third query example 
- The TAG field type is used for most fields as they are assumed to be exact match queries only. If you need partial or range matching, then a NUMERIC or STRING field should be used accordingly
