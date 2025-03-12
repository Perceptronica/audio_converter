# audio_converter


Пример установки:
```
uv venv init
source .venv/bin/activate
uv pip install -r requirements.txt
uv pip freeze > requirements.txt
mkdir temp
sudo su - postgres -c "initdb --locale en_US.UTF-8 -D /var/lib/postgres/data"
sudo systemctl start postgresql.service
sudo -u postgres createuser -P userr
sudo -u postgres createdb -O userr music_db
psql -U userr -d music_db -f ddl.sql
psql -U userr -d music_db -f ddl.sql
```
