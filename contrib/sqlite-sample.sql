-- Example configuration data (SQLite)
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
INSERT INTO server VALUES(3000,587,'smtp','primary-smtp.64f2f16209f14ec4a3fca8d306a6d66c.com','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(3001,587,'smtp','secondary-smtp.11bacc34ba224bfdbdb4cddd5780f904.com','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(3002,143,'imap','imap1.9ec2004c71ad4f5dbc5d1c9092768553.com','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(3003,143,'imap','imap2.85270c34b65c46c29b837e6fc1cdc72a.com','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(3004,123,'INVALID','578cef00f06e42beb31ce0fdb3159c6d.ham-n-eggs.tld','STARTTLS','%EMAILADDRESS%','plain');
CREATE TABLE domain (
	id INTEGER NOT NULL, 
	provider_id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(provider_id) REFERENCES provider (id), 
	UNIQUE (name)
);
INSERT INTO domain VALUES(2000,1000,'example.com');
INSERT INTO domain VALUES(2001,1000,'example.net');
INSERT INTO domain VALUES(2002,1000,'example.org');
INSERT INTO domain VALUES(2003,1001,'ham-n-eggs.tld');
INSERT INTO domain VALUES(2004,-2004,'orphan.tld');
INSERT INTO domain VALUES(2005,1002,'serverless.tld');
CREATE TABLE server_domain (
	server_id INTEGER NOT NULL, 
	domain_id INTEGER NOT NULL, 
	PRIMARY KEY (server_id, domain_id), 
	FOREIGN KEY(server_id) REFERENCES server (id), 
	FOREIGN KEY(domain_id) REFERENCES domain (id)
);
INSERT INTO server_domain VALUES(3001,2002);
INSERT INTO server_domain VALUES(3004,2003);
INSERT INTO server_domain VALUES(3002,2000);
INSERT INTO server_domain VALUES(3000,2000);
INSERT INTO server_domain VALUES(3000,2001);
INSERT INTO server_domain VALUES(3003,2001);
INSERT INTO server_domain VALUES(3003,2002);
COMMIT;
