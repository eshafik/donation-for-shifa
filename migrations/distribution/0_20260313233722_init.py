from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(45) NOT NULL UNIQUE,
    "email" VARCHAR(255) UNIQUE,
    "password" VARCHAR(255),
    "name" VARCHAR(100),
    "joined_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "last_login" TIMESTAMPTZ,
    "is_admin" BOOL NOT NULL DEFAULT False
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "donations" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "donor_name" VARCHAR(255) NOT NULL,
    "transaction_number" VARCHAR(100) NOT NULL UNIQUE,
    "amount" DECIMAL(12,2) NOT NULL,
    "date_received" DATE NOT NULL,
    "notes" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "donation_distributions" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "recipient_name" VARCHAR(255) NOT NULL,
    "address" TEXT NOT NULL,
    "problem_description" TEXT NOT NULL,
    "amount_received" DECIMAL(12,2) NOT NULL,
    "date_distributed" DATE NOT NULL,
    "notes" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmFtP2zAUx79K1adOYhULlLK9lbZAtF4mCBtimiw3OU0tEjs4zkqF+t1nO0lzpQO0S5"
    "F4qZK/z7HP+fnYsfvQdEgoOJlFgjDaHjCK1cMgJzY/NR6aFPsgH55gvddo4iAo2ypZ4JkX"
    "d5L4obxFqD1nUsC2kFZz7IUgJQdCm5MgiYRGnqdEZitP6mZSRMldBEgwF8QCuGz4/kPKhD"
    "pwD2H6GtyiOQHPKSRFHDW21pFYBVo7Ia5Jxam2VQPOkM28yKeZfbASC5lD6kCoUKoLFDgW"
    "oEYQPFIZqACT1NOk4mAzkzjKnI8Dcxx5IpfxEzHYkqREKKMJdY6uGuX9R8M4OOga+wdHx5"
    "3DbrdzvH8sbXVI1abuOk44AxJ3pbGYZ+bEUokyOU/xdCphrX2wwLGX5p0B5mCTgAAVSCsV"
    "2P0F5vWoq54l7DLZMvYU8jbuqZCBz+rtD5H38T3ygLpiIV+NTmcL1a+9i/5576Ilrd4V2U"
    "6SJiNuU5gzrNhxOIRhlacF94+Ubs7ltYDcws0aXuta9MPwzsvjao1715qkv0paRtPJWWqe"
    "w9sfTU9KVAPOZK4+yof7DMKPuL/RrqeNfRbJ1S3XOZCfULMRD+QO4GPvkXKuepdAO7F7O+"
    "nm1UEfDPvmuDdqfTD2DM1YEiYC8rvG4X55Y5AbMWQf11qq0qIeaZ1vmak0EcSHtnp4fUR7"
    "1rDEizIBz9pGNw4vWtbJN343cPyVVW1zUOkjLOpLT1VPPdmi57bCUw+7WXzy1IKdKfVWyV"
    "xvo2+Oh5dWb/ylMAWqRFWLUcCfqq2j0iFh00njm2mdN9Rr42Y6GWqCLBQu1yNmdtZNU8WE"
    "I8EQZUskTwVZWaZqCqYwsVHgvHBii55vE/tfJzYJvrpgZyv03NtQxfX3F6Od2BP/3dVIXT"
    "znt7U3owxeFfop40Bc+hlWGrwpo8fUrrsERSHw9pX82UnQ67RiUjWLguPl5j5eLST1DwF4"
    "EJ92LodWY3I1GjU1zhm2b5eYO6jAVbUwg5WUjW21yTf8soIpdjUGlcx6/QvTdIVN"
)
