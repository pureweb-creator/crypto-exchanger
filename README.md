# Exchange Bot

Half-working telegram bot for crypto exchange.

## Tech stack

- [aiogram](https://docs.aiogram.dev/) 3.x — Telegram Bot API
- PostgreSQL + [asyncpg](https://github.com/MagicStack/asyncpg) — users and orders
- Redis — FSM storage and exchange data cache
- [SQLAlchemy](https://docs.sqlalchemy.org/) 2.x (async) + [Alembic](https://alembic.sqlalchemy.org/) — ORM and migrations
- [Pydantic](https://docs.pydantic.dev/) — settings and validation

## Prerequisites

- Python 3.11+
- Docker
- Telegram Bot Token ([@BotFather](https://t.me/BotFather))

## Project structure

```
exchanger_bot/
├── alembic/               # Migrations
├── bot/
│   ├── core/config.py     # Pydantic settings
│   ├── database/models.py # SQLAlchemy models
│   ├── handlers/          
│   ├── keyboards/         
│   ├── middleware/        
│   ├── services/          # Business logic
│   ├── states/            # FSM states
│   ├── tasks/             # Asyncio tasks
│   ├── filters/
│   └── utils/
├── bot.py                 # Entry point
```

## Commands

- `/start` — Welcome and short description; registers user
- `/exchange` — Start the exchange flow (currency → pair → amount → order)