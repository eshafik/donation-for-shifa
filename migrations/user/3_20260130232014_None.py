from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(45) NOT NULL UNIQUE,
    "email" VARCHAR(255) UNIQUE,
    "password" VARCHAR(255),
    "name" VARCHAR(100),
    "joined_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "last_login" TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztl21v2jAQx79KlFed1FU0hML2Dli3Mq0wtexBnabIJCZ4dew0dtairt99PpOQJ2DQsd"
    "JWe4OSv+/iu9/hh7s1Y4Gjg0/qx3xt3JoMBVg95NR9w0RhmGrwKtGIzo2ENhgJGSFXKnGM"
    "qMBK8rBwIxJKwplSWUwpiNxVhoT5mRQzchVjR3Ify4kO4tt3JRPm4Rss0tfw0hkTTL1CjM"
    "SDubXuyGmotQ7xe0y+1bYw4chxOY0DltmHUznhbO5AmATVxwxHSGKYQUYxZAABJpmmSc2C"
    "zUxmUeZ8PDxGMZW5jNfE4HIGCFU0QufowywvX1lWvd60avWjVsNuNhutWkvZ6pCqQ827Wc"
    "IZkNmnNJbeu15/CIlyVadZ9UC40z5IopmX5l38E+jnCubuBEWLIed9SqhVgmXUKdidsg7Q"
    "jUMx8+VEvdqNFRg/t8+6J+2zPbvxosiyn4xYegioZhRxgAjdBOHc4V78Ejo7wmc11uGnrJ"
    "YC1GNFgiES4ppHC5b7coh5n61wTE0ykNlW92RIbrqa/2ol75rgYa22BkFltZSgHisS/MEJ"
    "w56DZBXjG4VCkgAvRllwLPH0Es+D9OE+++QD4I0w8gaMTpPirqA77J0enw/bpx8hk0CIK6"
    "oJtYfHMGJpdVpS945KhZh/xPjSG54Y8GpcDPrHmiAX0o/0jJnd8MKEmFAsucP4tYO83IaX"
    "qimYQlnjENDfp65Fz/+F3Wlhk+CzulIkpEO5T9imdS16bqGuD78dPpEypmlXFijc/MeXua"
    "spCCPkXl6jyHMqI9ziy2yrQ4EVlBXEkK/rADQhTt0EtXFE3IlZaY4SfX95e4Qyi0fTHz2j"
    "5sg6tJt2q35kz3uiubKqFfpz2/NTdbUQ0gb3pJzLdpqeZ3HbhIWxAcTE/GkC/CeXTTWjxG"
    "zBleT9+aC/GGLOpXxmEVcavwxKRGVRPw6gK/hBvoWTKsW2d9r+Wiba/TDolI8g+EBH0d3p"
    "kXL3G3IDLNU="
)
