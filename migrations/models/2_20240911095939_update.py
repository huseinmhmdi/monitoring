from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `alertresult` ADD `level` INT NOT NULL  DEFAULT 0;
        ALTER TABLE `alertresult` ADD `project_name` VARCHAR(191) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `alertresult` DROP COLUMN `level`;
        ALTER TABLE `alertresult` DROP COLUMN `project_name`;"""
