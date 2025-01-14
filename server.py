import logging
import random
import string
import time
import chromadb
import chromadb.config
from chromadb.server.fastapi import FastAPI, Request

logger = logging.getLogger(__name__)

settings = chromadb.config.Settings(
    chroma_db_impl = 'clickhouse',
    clickhouse_host ='clickhouse',
    clickhouse_port = 8123 
)

server = FastAPI(settings)
app = server.app()
app.debug = True

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response
