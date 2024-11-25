import random
import logging
from flask import Flask

app = Flask(__name__)

logging.basicConfig(
    filename='/var/log/app/app.log',
    level=logging.INFO,
    format='%(levelname)s - %(message)s',
    encoding='utf-8'
)

logger = logging.getLogger(__name__)

logger.info("Application started.")

@app.route("/dice", methods=["GET"])
def dice():
    dice_number = random.randint(1, 6)
    logger.info(f"Dice rolled: {dice_number}")
    return f'{dice_number}'

@app.route("/health", methods=["GET"])
def health():
    try:
        return "OK", 200
    except Exception as e:
        logger.error("Health check failed.", exc_info=True)
        return "Service is not ready yet", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
