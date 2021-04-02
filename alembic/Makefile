DBURI	= sqlite:////Users/ralph/projects/automx2/local/dev.sqlite
# Short message used when generating a new revision
MIGMSG	= DAV server support
# Environment variables
FLASKDB = PYTHONPATH=.. FLASK_APP=automx2.server:app flask db
# Shared Alembic options
ALOPTS	= -d .

.PHONY:	all prep migrate upgrade

all:
	@echo "Usage: make {migrate | upgrade}"

prep:
	sed -E -e 's,^(sqlalchemy.url =).*,\1 $(DBURI),' -i.bak alembic.ini

migrate:
	$(FLASKDB) migrate $(ALOPTS) -m "$(MIGMSG)"

upgrade:
	$(FLASKDB) upgrade $(ALOPTS)
