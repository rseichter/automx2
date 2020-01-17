PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE provider (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	short_name VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO provider VALUES(1000,'Big Corporation, Inc.','BigCorp');
INSERT INTO provider VALUES(1001,'Ham & Eggs','H+E');
INSERT INTO provider VALUES(1002,'Some Other Provider','SOP');
CREATE TABLE server (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	port INTEGER NOT NULL, 
	type VARCHAR NOT NULL, 
	socket_type VARCHAR NOT NULL, 
	user_name VARCHAR NOT NULL, 
	authentication VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO server VALUES(4000,'primary-smtp.fb994de7a5474925bb88e8efbabfe645.com',587,'smtp','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(4001,'secondary-smtp.4ed56b729c1144ab9a9b69f200f1df00.com',587,'smtp','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(4002,'imap1.61fcba7ba3a24141930d5e859960ed60.com',143,'imap','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(4003,'imap2.4c94160e7d5d4f8690f1f6b8080f9250.com',143,'imap','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(4004,'f4c7e165569b4dcf8925777b2abdf1e1.ham-n-eggs.tld',123,'INVALID','STARTTLS','%EMAILADDRESS%','plain');
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
INSERT INTO ldapserver VALUES(2000,'ldap.example.com',636,1,'ou=People,dc=example,dc=com','(mail={0})','uid','cn','secret','cn=automx2,ou=Tech,dc=example,dc=com');
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
INSERT INTO domain VALUES(3000,'example.com',1000,NULL);
INSERT INTO domain VALUES(3001,'example.net',1000,NULL);
INSERT INTO domain VALUES(3002,'example.org',1000,NULL);
INSERT INTO domain VALUES(3003,'ham-n-eggs.tld',1001,2000);
INSERT INTO domain VALUES(3004,'orphan.tld',-3004,NULL);
INSERT INTO domain VALUES(3005,'serverless.tld',1002,NULL);
CREATE TABLE server_domain (
	server_id INTEGER NOT NULL, 
	domain_id INTEGER NOT NULL, 
	PRIMARY KEY (server_id, domain_id), 
	FOREIGN KEY(server_id) REFERENCES server (id), 
	FOREIGN KEY(domain_id) REFERENCES domain (id)
);
INSERT INTO server_domain VALUES(4000,3000);
INSERT INTO server_domain VALUES(4000,3001);
INSERT INTO server_domain VALUES(4003,3001);
INSERT INTO server_domain VALUES(4003,3002);
INSERT INTO server_domain VALUES(4001,3002);
INSERT INTO server_domain VALUES(4004,3003);
INSERT INTO server_domain VALUES(4002,3000);
CREATE TABLE alembic_version (
        version_num VARCHAR(32) NOT NULL, 
        CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('f62e64b43d2f');
COMMIT;
