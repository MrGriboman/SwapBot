import aiosqlite
import sqlite3
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
name = os.getenv("db_name")


async def connect_to_db():
    con = await aiosqlite.connect(name)
    '''await cur.execute('CREATE TABLE if not exists "users" ("ID"	INTEGER NOT NULL UNIQUE, "Name"	TEXT NOT NULL, '
                      'PRIMARY KEY("ID"))')

    await cur.execute('CREATE TABLE if not exists "offers" ("offer_id"	INTEGER NOT NULL UNIQUE, "giver_id"	INTEGER '
                      'NOT NULL'
                      'UNIQUE,PRIMARY KEY("offer_id"),FOREIGN KEY("giver_id") REFERENCES "users"("ID"))')

    await cur.execute('CREATE TABLE if not exists "books" ("offer"	INTEGER NOT NULL UNIQUE,"booker_id"	INTEGER NOT '
                      'NULL UNIQUE,"time"	INTEGER NOT NULL,PRIMARY KEY("offer","booker_id"),FOREIGN KEY("offer") '
                      'REFERENCES "offers"("offer_id"),FOREIGN KEY("booker_id") REFERENCES "users"("ID"))')'''

    # await con.commit()
    return con


async def add_user(con, user_id, user_name):
    cur = await con.cursor()
    await cur.execute(f"INSERT INTO users (ID, Name) VALUES ({user_id}, '{user_name}')")
    await con.commit()
    await cur.close()


async def add_offer(con, offer_id, giver_id, description):
    cur = await con.cursor()
    await cur.execute(f"INSERT INTO offers (offer_id, giver_id, description) VALUES ({offer_id}, {giver_id}, '{description}')")
    await con.commit()
    await cur.close()


async def add_book(con, offer_id, booker_id, time):
    cur = await con.cursor()
    await cur.execute(f"INSERT INTO books (offer_id, booker_id, time) VALUES ({offer_id}, {booker_id}, {time})")
    await con.commit()
    await cur.close()


async def get_offers_list(con, giver_id):
    cur = await con.cursor()
    res = await cur.execute(f"SELECT description FROM offers WHERE giver_id = {giver_id}")
    return res
