import logging 
import sys 
from src.ingestion import run_ingestion
from src.transform import run_transform
from src.config import TICKERS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("== Pipeline run started ==")
    
    try: 
        run_ingestion(TICKERS)
    except Exception as e:
        logger.error(f"Pipeline aborted: ingestion failed entirely - {e}")
        sys.exit(1) # non-zero exit code: signals failure to anything watching
        
    try:
        run_transform(TICKERS)
    except Exception as e:
        logger.error(f"Pipeline aborted: transform failed - {e}")
        sys.exit(1)
    
    logger.info("=== Pipeline run completed successfully ===")
    sys.exit(0) # explicit success signal 

if __name__ == "__main__":
    main()