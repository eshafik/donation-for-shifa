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
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztl21P2zAQgP9KlU+dxKoSKGX7VtoC0foyQdgQ0xS5yTW1SOziOIMK9b/PdpImTkIHiG"
    "2dtG/2vcR3j+9s59HwKEEcU9IapAPjY+PRICgEMajR7jUMtFwWdVLE0SzQHCJlOIs4Qy4X"
    "ijkKIhAiDyKX4WW6EImDQAqpKwwx8XNRTPBdDA6nPvAFMKH49l2IMfHgAaJsurx15hgCT4"
    "sZe3JtJXf4aqlkJ9i3CD9VtnLBmePSIA5Jbr9c8QUlGwdMuJT6QIAhDnIFzmKZgQwwzTZL"
    "Kgk2N0miLPh4MEdxwAsZPxODK0gKhCKaSOXoy1XefzDNg4Ou2T44Ou4cdrud4/axsFUhVV"
    "XddZJwDiT5lMJinVkTWyZKxT4lOygFa+WDOEq8FG+tKChz1KwCur9ArB6z7lXCLZIs487g"
    "buOdCXLgeZ29EfEQPTgBEJ8vxNTsdLbQ/NK76J/3LprC6p3OdJKqzEQn8eY4xWokEl0iIn"
    "NIHM6AvQRrvffb4P3t5azB3W+3nwFXWD0JV+l0uCikcdLKOtABuDhEQT3T3KnE0Uu8Wqn3"
    "bpbsFoiDYd8a90bNfXPPVBSjuwBzKPI9rCAU5wA4DFzAP6DmaB0I9RMdX3Ys0xR6jkNoyc"
    "G/x7JnD0ukCOUQVQnZ8PDE1bNxeFW/pt24Gzjs4bW6SMJI1FSxLZvj3rWqtXCVakbTyVlm"
    "Xmjj/mh6UgLqMpDpO6iug9PqqSere24rPDnYzeIzRA7elASrdK+30bfGw0u7N/6sbYEsUa"
    "kxNfyZtHlUOkg3H2l8tezzhpw2bqaToSJII+4ztWJuZ98YMiYUc+oQeu8gr3BJZNIMjLax"
    "8dJ75cbqnv839q9ubBp8tWFnK+elz/CK669f5DtxJv65N7n845nf1j7Jc3hV6KeUAfbJJ1"
    "gp8JaIHhG37hUeR8BaVxHs9OWTS/MoGLrf/AhWC0lk6EEAyTvncmg3JlejkaFwzpB7e4+Y"
    "52hcpYaatCTZ2FZVoRmWJYggX2GQyazXPwEdXfF4"
)
