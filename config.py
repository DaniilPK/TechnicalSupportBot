from sqlalchemy import URL

BOT_TOKEN=''
DatabaseConfig = postgre_url = URL.create(
        'postgresql+asyncpg',
        username='' ,
        password='',
        host="",
        database='',
        port=5432
    )
chatID=CHAT_ID