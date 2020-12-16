-- SQLite schema definition
CREATE TABLE provider (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	short_name VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE server (
	id INTEGER NOT NULL, 
	prio INTEGER DEFAULT '10' NOT NULL, 
	name VARCHAR NOT NULL, 
	port INTEGER NOT NULL, 
	type VARCHAR NOT NULL, 
	socket_type VARCHAR NOT NULL, 
	user_name VARCHAR NOT NULL, 
	authentication VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE ldapserver (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	port INTEGER NOT NULL, 
	use_ssl BOOLEAN NOT NULL, 
	search_base VARCHAR NOT NULL, 
	search_filter VARCHAR NOT NULL, 
	attr_uid VARCHAR NOT NULL, 
	attr_cn VARCHAR, 
	bind_password VARCHAR, 
	bind_user VARCHAR, 
	PRIMARY KEY (id), 
	CHECK (use_ssl IN (0, 1))
);
CREATE TABLE domain (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	provider_id INTEGER NOT NULL, 
	ldapserver_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	FOREIGN KEY(provider_id) REFERENCES provider (id), 
	FOREIGN KEY(ldapserver_id) REFERENCES ldapserver (id)
);
CREATE TABLE server_domain (
	server_id INTEGER NOT NULL, 
	domain_id INTEGER NOT NULL, 
	PRIMARY KEY (server_id, domain_id), 
	FOREIGN KEY(server_id) REFERENCES server (id), 
	FOREIGN KEY(domain_id) REFERENCES domain (id)
);
