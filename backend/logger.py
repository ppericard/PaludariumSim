import logging
import sys
import config

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a logger with the specified name and configuration.
    """
    logger = logging.getLogger(name)
    
    # Set level based on config
    level_str = getattr(config, "LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_str, logging.INFO)
    logger.setLevel(level)
    
    # Create console handler if not already added
    if not logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s', datefmt='%H:%M:%S')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File Handler
        try:
            import os
            import datetime
            
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # Generate timestamped filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"server_{timestamp}.log"
            
            # Use FileHandler for unique file per run
            file_handler = logging.FileHandler(
                os.path.join(log_dir, log_filename),
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG) # Always log debug to file
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Failed to setup file logging: {e}")
        except Exception as e:
            print(f"Failed to setup file logging: {e}")
        
    return logger
