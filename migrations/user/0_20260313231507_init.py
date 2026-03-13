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
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztl21v2jAQx79KxKtO6ioaoLC9Ix1bmQpMLd2mTlNkEhO8OnYaO21R1+8+n0nIEzDo2t"
    "JWe4OSv+/iu9/h5O62Egkc7p2pn8p747bCkI/VRUbdNSooCBINbiUa0bmR0AYjIUPkSCWO"
    "ERVYSS4WTkgCSThTKosoBZE7ypAwL5UiRi4jbEvuYTnRQfz4qWTCXHyDRXIbXNhjgqmbi5"
    "G4sLfWbTkNtGYRr8vkR20LG45sh9PIZ6l9MJUTzuYOhElQPcxwiCSGHWQYQQYQYJxpktQs"
    "2NRkFmXGx8VjFFGZyXhNDA5ngFBFI3SOHuzy9p1p1mpNs1o7aDXqzWajVW0pWx1Seal5N0"
    "s4BTJ7lMbS/dTtDyFRruo0qx4Id9oHSTTz0rzzfwJ9XcJ8OEHhYshZnwJqlWARdQJ2q6x9"
    "dGNTzDw5Ubf1xgqMX9snh0ftk516402eZT9eMfUSUE0pYh8RugnCucO9+MV0toTPbKzDT1"
    "ktBajX8gQDJMQ1Dxcc9+UQsz4PwjExSUGmr7oXQ3LT0/xPJ3nbBPer1TUIKqulBPVanuAv"
    "Thh2bSTLGD8oFJL4eDHKnGOBpxt77iUX93lPPgHeECN3wOg0Lu4KusNur3M6bPe+QCa+EJ"
    "dUE2oPO7BianVaUHcOCoWYP8T41h0eGXBrnA/6HU2QC+mFesfUbnhegZhQJLnN+LWN3MwL"
    "L1ETMLmyRgGgv09d857/C7vVwsbBp3WlSEibco+wTeua93yAuj796/CFlDFJe+UBJUJZ+4"
    "vKaHFOMWJLev6MW6GGI+X3WMdx0ylo/cJZg8FxrmZWt9DX9896Vkd913SxlBGRmXYfhqnx"
    "RabbB2GEnItrFLp2aYWbfJlteck3/aKCGPI0IsgTstJzZRuHxJlUSvNmrO8unzhRavFsRs"
    "5XNG+a+/VmvVU7qM/HzLmyarr8+yR5hUMBIW3QemZcHmaOfBUNPByMDSDG5i8T4KP072pH"
    "idmCLu/z6aC/GGLGpdgGEEcavw1KROlQPw+gK/hBvrkPSYJtp9f+XiR6eDywil91eIC17U"
    "/K3R/CGJiW"
)
