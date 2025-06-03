import os
import sys

# Добавляем корневую директорию проекта (где находится папка app) в sys.path
# Это позволяет Alembic находить ваши модули приложения.
# Путь рассчитывается относительно текущего файла (env.py)
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_DIR)

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine # Import AsyncEngine

from qalembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ensure all models are imported by importing the app's central base module
# This loads model definitions (e.g., User) and registers them with Base.metadata
import app.db.base 

from app.db.base_class import Base # Adjusted import path
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )
    # For async, we need to create an AsyncEngine
    configuration = config.get_section(config.config_ini_section)
    # It's better to get the URL from our app's config to ensure consistency
    # For now, using the one from alembic.ini as fallback
    db_url = configuration.get("sqlalchemy.url")
    if not db_url:
        from app.core.config import settings # Adjusted import path
        db_url = settings.DATABASE_URL

    connectable = AsyncEngine(
        engine_from_config(
            configuration, # use the whole section
            prefix="sqlalchemy.", # prefix for sqlalchemy keys
            poolclass=pool.NullPool,
            # future=True # future is True by default in SQLAlchemy 2.0
            url=db_url # Ensure we are using the correct URL
        ).url # Get the URL object from the sync engine
    )


    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online()) 