from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `monitor` MODIFY COLUMN `source_id` INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `monitor` MODIFY COLUMN `source_id` INT NOT NULL;"""
