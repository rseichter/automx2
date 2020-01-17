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
	port INTEGER NOT NULL, 
	type VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	socket_type VARCHAR NOT NULL, 
	user_name VARCHAR NOT NULL, 
	authentication VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO server VALUES(4000,587,'smtp','primary-smtp.3eafb80a87534a06b5d7c33ae6d86171.com','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(4001,587,'smtp','secondary-smtp.de759f926a7f42758b70d5ba7d4caabe.com','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(4002,143,'imap','imap1.0b23758ef27941d996d44d74a3542f75.com','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(4003,143,'imap','imap2.63dcd91a5e07468a8592473663d24ebd.com','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(4004,123,'INVALID','43a78ce21f144c3daf119223c018ce18.ham-n-eggs.tld','STARTTLS','%EMAILADDRESS%','plain');
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
INSERT INTO ldapserver VALUES(2000,'ldap.example.com',636,1,'ou=People,dc=example,dc=com','(mail={0})','uid','cn','SECRET','cn=automx2,dc=example,dc=com');
CREATE TABLE domain (
	id INTEGER NOT NULL, 
	provider_id INTEGER NOT NULL, 
	ldapserver_id INTEGER, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(provider_id) REFERENCES provider (id), 
	FOREIGN KEY(ldapserver_id) REFERENCES ldapserver (id), 
	UNIQUE (name)
);
INSERT INTO domain VALUES(3000,1000,2000,'example.com');
INSERT INTO domain VALUES(3001,1000,NULL,'example.net');
INSERT INTO domain VALUES(3002,1000,NULL,'example.org');
INSERT INTO domain VALUES(3003,1001,NULL,'ham-n-eggs.tld');
INSERT INTO domain VALUES(3004,-3004,NULL,'orphan.tld');
INSERT INTO domain VALUES(3005,1002,NULL,'serverless.tld');
CREATE TABLE server_domain (
	server_id INTEGER NOT NULL, 
	domain_id INTEGER NOT NULL, 
	PRIMARY KEY (server_id, domain_id), 
	FOREIGN KEY(server_id) REFERENCES server (id), 
	FOREIGN KEY(domain_id) REFERENCES domain (id)
);
INSERT INTO server_domain VALUES(4004,3003);
INSERT INTO server_domain VALUES(4000,3000);
INSERT INTO server_domain VALUES(4002,3000);
INSERT INTO server_domain VALUES(4000,3001);
INSERT INTO server_domain VALUES(4003,3001);
INSERT INTO server_domain VALUES(4001,3002);
INSERT INTO server_domain VALUES(4003,3002);
COMMIT;
