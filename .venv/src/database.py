import aiosqlite
import sqlite3
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
name = os.getenv("db_name")


async def connect_to_db():
    print('connect')
    con = await aiosqlite.connect(name)
    cur = await con.cursor()
    await cur.execute('CREATE TABLE if not exists "users" ("ID"	INTEGER NOT NULL UNIQUE, "Name"	TEXT NOT NULL, PRIMARY KEY("ID"))')

    await cur.execute('CREATE TABLE if not exists "offers" ("offer_id"	INTEGER NOT NULL UNIQUE, "giver_id"	INTEGER NOT NULL UNIQUE, "description" TEXT, PRIMARY KEY("offer_id"),FOREIGN KEY("giver_id") REFERENCES "users"("ID"))')

    await cur.execute('CREATE TABLE if not exists "books" ("offer"	INTEGER NOT NULL UNIQUE,"booker_id"	INTEGER NOT NULL UNIQUE,"time"	INTEGER NOT NULL,PRIMARY KEY("offer","booker_id"),FOREIGN KEY("offer") REFERENCES "offers"("offer_id"),FOREIGN KEY("booker_id") REFERENCES "users"("ID"))')

    await con.commit()
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


async def get_offers_list(con, giver_id, offset):
    cur = await con.cursor()
    res = await cur.execute(f"SELECT description, offer_id FROM offers WHERE giver_id = {giver_id} LIMIT 10 OFFSET {offset}")
    return res


async def offer_by_id(con, message_id):
    cur = await con.cursor()
    res = await cur.execute(f"SELECT offer_id FROM offers WHERE offer_id = {message_id}")
    return res


async def get_first_for_offer(con, offer_id):
    cur = await con.cursor()
    res = await cur.execute(f"SELECT booker_id FROM books WHERE offer_id = {offer_id} ORDER BY time LIMIT 1")
    return res


async def get_books_list(con, user_id, offset):
    cur = await con.cursor()
    res = await cur.execute(f"SELECT o.description, b.offer_id, b.booker_id from offers o JOIN books b on o.offer_id = b.offer_id WHERE b.booker_id = {user_id} LIMIT 1 OFFSET {offset}")
    return res


async def get_book(con, offer, booker):
    cur = await con.cursor()
    res = await cur.execute(f"SELECT o.description from offers o JOIN books b on o.offer_id = b.offer_id WHERE b.booker_id = {booker} AND b.offer_id = {offer}")
    return res


async def delete_book(con, offer, booker):
    cur = await con.cursor()
    await cur.execute(f"DELETE FROM books WHERE offer_id={offer} AND booker_id={booker}")
    await con.commit()
    await cur.close()
