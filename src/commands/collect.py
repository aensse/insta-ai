import logging
from src.main import bot

@bot.command(help="Collecting pending messages to database.")
def collect():
    logging.info("Soon!")
    