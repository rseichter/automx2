CREATE TABLE provider (
	id INTEGER NOT NULL, 
	name VARCHAR(128) NOT NULL, 
	short_name VARCHAR(32) NOT NULL,
	sign BOOLEAN DEFAULT 0 NOT NULL,
	sign_cert TEXT null,
	sign_key TEXT null,
	PRIMARY KEY (id)
);
CREATE TABLE server (
	id INTEGER NOT NULL, 
	prio INTEGER DEFAULT '10' NOT NULL, 
	name VARCHAR(128) NOT NULL, 
	port INTEGER NOT NULL, 
	type VARCHAR(32) NOT NULL, 
	socket_type VARCHAR(32) NOT NULL, 
	user_name VARCHAR(64) NOT NULL, 
	authentication VARCHAR(32) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE davserver (
	id INTEGER NOT NULL, 
	url VARCHAR(128) NOT NULL, 
	port INTEGER NOT NULL, 
	type VARCHAR(32) NOT NULL, 
	use_ssl BOOLEAN NOT NULL, 
	domain_required BOOLEAN NOT NULL, 
	user_name VARCHAR(64), 
	PRIMARY KEY (id), 
	CHECK (use_ssl IN (0, 1)), 
	CHECK (domain_required IN (0, 1))
);
CREATE TABLE ldapserver (
	id INTEGER NOT NULL, 
	name VARCHAR(128) NOT NULL, 
	port INTEGER NOT NULL, 
	use_ssl BOOLEAN NOT NULL, 
	search_base VARCHAR(128) NOT NULL, 
	search_filter VARCHAR(128) NOT NULL, 
	attr_uid VARCHAR(32) NOT NULL, 
	attr_cn VARCHAR(32), 
	bind_password VARCHAR(128), 
	bind_user VARCHAR(128), 
	PRIMARY KEY (id), 
	CHECK (use_ssl IN (0, 1))
);
CREATE TABLE domain (
	id INTEGER NOT NULL, 
	name VARCHAR(128) NOT NULL, 
	provider_id INTEGER NOT NULL, 
	ldapserver_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	FOREIGN KEY(provider_id) REFERENCES provider (id), 
	FOREIGN KEY(ldapserver_id) REFERENCES ldapserver (id)
);
CREATE TABLE davserver_domain (
	davserver_id INTEGER NOT NULL, 
	domain_id INTEGER NOT NULL, 
	PRIMARY KEY (davserver_id, domain_id), 
	FOREIGN KEY(davserver_id) REFERENCES davserver (id), 
	FOREIGN KEY(domain_id) REFERENCES domain (id)
);
CREATE TABLE server_domain (
	server_id INTEGER NOT NULL, 
	domain_id INTEGER NOT NULL, 
	PRIMARY KEY (server_id, domain_id), 
	FOREIGN KEY(server_id) REFERENCES server (id), 
	FOREIGN KEY(domain_id) REFERENCES domain (id)
);
