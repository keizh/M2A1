import logging 
import structlog
from src.core.config import setting
import sys

def set_up_logging()->None:
    # step 1
    sharedProcesses=[
        structlog.stdlib.add_log_level,
        # structlog.stdlib.add_log_level_number,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt='iso',utc=False),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    
    working_environment=setting.environment
    
    # step 2
    if working_environment == 'dev' or  working_environment == 'test':
        logging_area=structlog.dev.ConsoleRenderer()
    else:
        logging_area= structlog.processors.JSONRenderer()
        
    # step 3
    structlog.configure(
        processors=sharedProcesses+[logging_area],
         wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # step 4
    formatter=structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=sharedProcesses,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            logging_area
        ]
    )
    
    handler=logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root_logger=logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    
    # step 5
    for _log in ["uvicorn","uvicorn.error","uvicorn.access"]:
        uvicorn_logger=logging.getLogger(_log)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.propagate=True
    
    
logger = structlog.get_logger('app')