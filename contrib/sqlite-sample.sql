PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE provider (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	short_name VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO provider VALUES(100,'Example Inc.','Example');
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
INSERT INTO server VALUES(121,2,'imap.example.com',993,'imap','SSL','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(122,5,'pop.example.com',995,'pop','SSL','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(123,6,'pop.example.com',110,'pop','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(124,1,'smtp.example.com',587,'smtp','STARTTLS','%EMAILADDRESS%','plain');
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
INSERT INTO ldapserver VALUES(120,'ldap.example.com',636,1,'dc=foobar,dc=tld','(mail={0})','uid','cn','SECRET','cn=automx2,dc=example,dc=com');
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
INSERT INTO domain VALUES(110,'example.com',100,NULL);
CREATE TABLE server_domain (
	server_id INTEGER NOT NULL, 
	domain_id INTEGER NOT NULL, 
	PRIMARY KEY (server_id, domain_id), 
	FOREIGN KEY(server_id) REFERENCES server (id), 
	FOREIGN KEY(domain_id) REFERENCES domain (id)
);
INSERT INTO server_domain VALUES(121,110);
INSERT INTO server_domain VALUES(122,110);
INSERT INTO server_domain VALUES(123,110);
INSERT INTO server_domain VALUES(124,110);
COMMIT;
