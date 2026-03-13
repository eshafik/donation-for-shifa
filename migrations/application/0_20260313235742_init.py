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
);
CREATE TABLE IF NOT EXISTS "donation_applications" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "applicant_name" VARCHAR(255) NOT NULL,
    "applicant_phone" VARCHAR(30),
    "applicant_address" TEXT NOT NULL,
    "problem_description" TEXT NOT NULL,
    "amount_requested" DECIMAL(12,2),
    "status" VARCHAR(20) NOT NULL DEFAULT 'pending',
    "admin_notes" TEXT,
    "submitted_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "reviewed_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "donation_applications"."status" IS 'PENDING: pending\nREVIEWED: reviewed\nAPPROVED: approved\nREJECTED: rejected';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmG1P4kAQx78K4RWXeIQrop7vEKr2jqdgfYjnpVnaoezZbut2KxLDd7/dbUuhLSjmol"
    "ziG9L+d6Y785th+vBcRr7vYBMx7JFq2yPyoJlq5ePSc5kgF/jBi7Z70iRjKVSGRo68ghV7"
    "GUsGgfQbBYwik3GjMXIC4JIFgUmxH0dBQscRomdyQ0zsVAoJfgjBYJ4NbAKUL/z6zWVMLH"
    "iCIDn1740xBsdaSQhbYm+pG2zmS+0E2xphp9JWbDgyTM8JXZLa+zM24SkkDpgwodpAgCIG"
    "YgdGQ5GBCDDOPEkqCjY1iaJc8rFgjEKHLWX8SgwmJ8kR8mgCmaMtdvn6XVHq9UOlVj84au"
    "wfHjaOakfcVoaUXzqcRwmnQKJLSSzamdbTRaIer1NUTSHMpQ9iKPKSvHMdQ5ghlRzs1gTR"
    "YtR5zwx2nmwWewJ5E/dESMGn/faPyLvoyXCA2GzCT5VGYwPVq+awdd4cVrjVl1W2vXhJid"
    "YE5iKsPkfyRq4L1zeBjdv1w7jWa6/AWq+tpSqW1kFFlkUhCPJYdXhaMxkKnf+Xjt1AUldv"
    "5J/eDYIHZ5lgpdu8kXDdWbzS6ffOEvMl4q1O/yRD2qcez9U1lsPdgvUa90/axbSR64W8Ly"
    "nwBAMBIoe6DSZ2kbOmswvcM6ityL8aX2cnp8cG6m21pXWbnco3ZU+RkDlizGB5kOznpkXA"
    "EAsLRoSYvCoJXQlT4yEgYkIOaur9fl1b9oFYAlEOYnmg9tpa7+y4FJvckaF6panXavu4RO"
    "ERwxSsO9IcDIb9K6HxaUe9R6EN1R9qS4/s/oAZ98fWN8nXDHNl/TBX8sPccjExiMdguzG+"
    "6vaf3Bnfe6IE4cjFjAMwECuYJhwNwy4UE876ZkdJ7FxNDnZzhpcpIKtPnFlc700V0Lrqhd"
    "7sDlbK0G7qqlhRVkqQqJWDTKsvLlK61vTzkjgt3fZ7qiToBcymcsfUTr8ti5hQyDzezlPx"
    "VJK2ZqImYFaKG/oC/VtKu+r5WdgPLWwcfFrXZI4bo5mx7Xtv3vfld+CdmIzv9xYsvjGM7w"
    "tfgpfo5bGfehSwTX7CLPfEkGEcBkCrl/xnJ0nPk55J1DQKiqaLby8FrcRTtMCB6IHrQtVL"
    "vctOpyyBjpB5P0XUMlbIihVP8TLKwja/5CpuVkEE2ZKDyGY+/wsTNCJl"
)
