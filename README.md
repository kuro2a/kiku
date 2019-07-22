# KIKU - Light weight metrics monitoring tool -

## 開発者メモ

個人で運用しているシステムインフラの監視を行うにあたり、ZABBIXやELKスタック、その他ソリューションを導入/構築することが面倒だったため、新規で作成したものです。今後、ミドルウェアやアプリケーション自体も監視対象に入れることを予定しています。

開発言語にPython3を、フレームワークとしてFalcon2を採用しています。 

## Screenshots

![Screen Shot](/screenshot/v0.0.1-1.png "Screen Shot")
![Screen Shot](/screenshot/v0.0.1-2.png "Screen Shot")

## How to instration

```
$ # For server
$ pip3 install falcon jinja2 bcrypt pymongo tinydb redis pytest sqlalchemy psycopg2 pymysql
$ python3 main.py
$ # For collector 
$ pip3 insatall paramiko bcrypt pymongo sqlalchemy psycopg2 pymysql pytest
$ python3 collector.py
$ crontab -e
* * * * * ~/kiku/collector.py 1>/dev/null 2>&1
```

### Database engine configuration

#### For system information database(RDBMS).
- SQLite3
  - Example: `sqlite:///data/db.sqlite`
  - Example: `sqlite://:memory:` *For DEBUG only.
- PostgreSQL
  - Example: `postgresql://kiku:K1kuPassWd@localhost/kiku`
  ```sql
  $ psql -h localhost -U postgres
  > CREATE DATABASE kiku;
  > CREATE USER kiku WITH PASSWORD 'K1kuPassWd';
  ```
- MySQL
  - Example: `mysql+pymysql://kiku:K1kuPassWd@localhost/kiku`
  ```sql
  $ mysql --host localhost --user root --password
  > CREATE DATABASE kiku;
  > CREATE USER kiku;
  > GRANT ALL ON kiku.* TO kiku IDENTIFIED BY 'K1kuPassWd';
  > FLUSH PRIVILEGES;
  ```
- Oracle (option)
  - Example: `oracle+cx_oracle://kiku:K1kuPassWd@localhost:1521/kiku`
- SQLServer (option)
  - Example: `mssql+pyodbc://kiku:K1kuPassWd@mydsn`
  - Example: `mssql+pymssql://kiku:K1kuPassWd@localhost:1433/kiku`


#### For log database(DocumentDB).
- TinyDB
  - Example: `tinydb:///data/document.json`
- MongoDB
  - Example: `mongodb://localhost:27017`


# JSON API reference

## Common information for all APIs

### HTTP Request

|item|description|notes|
|---|---|---|
|Method|GET||
|Path|/api/{version}/{resqource}/...||

|value|type|format|description|notes|
|---|---|---|---|---|
|version|string|v1|API version.||
|resource|string|*|Target resouce name to get data.||

### HTTP Response

```
{
    "meta": {
        "status": "OK",
        "message": "OK",
        "timestamp": "YYYY/mm/dd HH:MM:SS"
    },
    "data": {
        ...
    }
}
```

|property|type|description|notes|
|---|---|---|---|
|meta|object|Meta data of response to the request.||
|meta.status|string|The response messages from server.||
|meta.timestamp|string|The timestamp that service response.||
|data|object|Response data.||



# Libraries

- falcon (Main framework)
  - https://falconframework.org/
- SQLAlchemy (ORM)
  - https://www.sqlalchemy.org/
- Jinja2 (Template engine)
  - http://jinja.pocoo.org/
- UIKit (CSS framework)
  - https://getuikit.com/
- c3.js and d3.js (SVG based JavaScript chart library)
  - https://c3js.org/
  - https://d3js.org/
- moment.js (JavaScript datetime library)
  - https://momentjs.com/
- axios.js (Promise based JavaScript HTTP client library)
  - https://github.com/axios/axios

And more.

Many thanks to all developers of these libraries.
