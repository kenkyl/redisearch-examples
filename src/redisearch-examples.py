# NOTE: importing the redisearch client is separate library from the standard redis client
import redis
import redisearch
import random
import time

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

def main():
    ## 0. connect to Redis (NOTE: redis_client added for example and is not needed if only using RediSearch commands)
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset='utf-8', decode_responses=True)
    rsearch_client = redisearch.Client('session_index', host=REDIS_HOST, port=REDIS_PORT)

    ## 0. test Redis connection
    print(redis_client.ping())

    ## 1. create the index with FT.CREATE
    try:
        rsearch_client.create_index((
            redisearch.TagField('app_oid', no_index=True), # NOTE: no_index = true for fields that do not need to be indexed 
            redisearch.TagField('vnf_id'),
            redisearch.TagField('thread_id'),
            redisearch.NumericField('timestamp', sortable=True), # NOTE: sortable = true for sortable fields 
            redisearch.TagField('ktab') 
        ))
    except redis.exceptions.ResponseError:
        print('index already exists')
    
    ## 2. add documents with FT.ADD
    add_documents(rsearch_client)

    ## 3. query the documents with FT.SEARCH
    interval = 3

    ## 3.a -- search for all session documents with ktab = 1 
    res = rsearch_client.search('@ktab:{1}')
    print(f'Session documents with ktab=1:\n{res}\n')
    time.sleep(interval)

    ## 3.b -- search for all session documents with ktab = 2, vnf = 2
    res = rsearch_client.search('@ktab:{2} @vnf_id:{2}')
    print(f'Session documents with ktab=2, vnf = 2:\n{res}\n')
    time.sleep(interval) 

    ## 3.c -- seach for all session documents with ktab = 3, timestamp > (now - 5 sec), sort by timestamp (asc)
    # NOTE: for complex queries, create an instance of the Query object
    query_string = '@ktab:{3} @timestamp:[' + str(int(time.time()) - 5000) + '+inf]'
    query = redisearch.Query(query_string).sort_by('timestamp', asc=True)
    res = rsearch_client.search(query)
    print(f'Session documents with ktab = 3, timestamp > (now - 5 sec):\n{res}\n')
    

def add_documents(rsearch_client):
    start_index = random.randint(0, 1000) # pick a random number 0-1000 to create sequential ids for the session documents
    # add 10 documents to the index 
    for i in range(start_index, start_index+9):
        # NOTE: FT.ADD called here
        try:
            res = rsearch_client.add_document(
                f'session:{i}',
                app_oid = str(random.randint(1,3)),
                vnf_id = str(random.randint(1,3)),
                thread_id = str(random.randint(1,3)),
                timestamp = str(int(time.time())), 
                ktab = str(random.randint(1,3))
            )
        except redis.exceptions.ResponseError:
            print('document already in index')

if __name__ == "__main__":
    main()