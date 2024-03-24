import os.path
import sys

import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Context, CommandSyncFlags
from dotenv import load_dotenv

from Daemon.OnMessageListener import OnMessageListener
from Daemon.bot_settings import *
from Daemon.constant import *

""" CONST ZONE """
# BOT TO RUN
RUNNING_MAIN_BOT = False
""" CONST ZONE END """

# 토큰들 가져오고, 세팅하기
if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/.env"):
    sys.exit("'.env' not found! Please add it and try again.")

load_dotenv()
if RUNNING_MAIN_BOT:
    token = os.environ.get('MAIN_BOT')
    bot_settings = get_main_settings(token)
else:
    token = os.environ.get('TEST_BOT')
    bot_settings = get_test_settings(token)


# 로거 세팅하기
class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
logger.setLevel(bot_settings.logger_settings)

# logging console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# file handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


class BlueBot(commands.InteractionBot):
    def __init__(self, intents, owner_ids, command_sync_flags, test_guilds):
        super().__init__(
            intents=intents,
            owner_ids=owner_ids,
            command_sync_flags=command_sync_flags,
            test_guilds=test_guilds
        )
        self.logger = logger
        self.logger.info("-----bot init-----")

    @tasks.loop(seconds=5)
    async def status_message(self):
        await self.change_presence(status=disnake.Status.online, activity=disnake.Game(next(blue_bot_message)))

    async def load_commands(self):
        """
        load commands from Commands folder
        """
        self.logger.info("-----loading commands-----")
        for filename in os.listdir("Commands"):
            if filename.endswith(".py"):
                self.load_extension(f"Commands.{filename[:-3]}")
                self.logger.info(f"Commands.{filename[:-3]}")
        self.logger.info("-----commands loaded-----")

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {disnake.__version__}")
        self.logger.info(f"Python version: {sys.version}")
        self.logger.info(f"Running on: {sys.platform}")
        self.logger.info("-------------------")
        await self.load_commands()
        self.logger.info("-----starting bot-----")
        self.status_message.start()

    async def on_message(self, message):
        if message.author.bot:
            return
        await OnMessageListener.alert(message)

    async def on_command_completion(self, ctx: Context) -> None:
        full_command_name = ctx.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        if ctx.guild is None:
            self.logger.info(f"{ctx.author} executed {executed_command} in DM")
        else:
            self.logger.info(f"{ctx.author} executed {executed_command} in guild {ctx.guild.name}")

    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        self.logger.error(error)
        raise error


command_sync_flags = CommandSyncFlags.all()

bot = BlueBot(
    intents=disnake.Intents.all(),
    owner_ids=set(owners),
    command_sync_flags=command_sync_flags,
    test_guilds=None
)

bot.run(bot_settings.token)
