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
INSERT INTO provider VALUES(1002,'HORUS-IT Ralph Seichter','HORUS-IT');
INSERT INTO provider VALUES(1003,'Some Other Provider','SOP');
INSERT INTO provider VALUES(1004,'sys4 AG','sys4');
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
INSERT INTO server VALUES(3000,587,'smtp','primary-smtp.04f7422c16fc477c87db7df22ac78859.com','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(3001,587,'smtp','secondary-smtp.075306d310734633a951373b0a61885a.com','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(3002,143,'imap','imap1.795f011809de4bd59f56701a74ce9ed1.com','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(3003,143,'imap','imap2.28026636ebf04c2d8d3fe12575c23ad0.com','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(3004,993,'imap','imap.horus-it.com','SSL','%EMAILLOCALPART%','plain');
INSERT INTO server VALUES(3005,587,'smtp','smtp.horus-it.com','STARTTLS','%EMAILLOCALPART%','plain');
INSERT INTO server VALUES(3006,143,'imap','mail.sys4.de','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(3007,587,'smtp','mail.sys4.de','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(3008,123,'INVALID','7465997e1fd34e93a8f433a3b1accc2a.ham-n-eggs.tld','STARTTLS','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(3009,993,'imap','imap.automx.org','SSL','%EMAILADDRESS%','plain');
INSERT INTO server VALUES(3010,587,'smtp','smtp.automx.org','STARTTLS','%EMAILADDRESS%','plain');
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
INSERT INTO domain VALUES(2003,1004,'automx.org');
INSERT INTO domain VALUES(2004,1002,'horus-it.de');
INSERT INTO domain VALUES(2005,1002,'horus-it.com');
INSERT INTO domain VALUES(2006,1004,'sys4.de');
INSERT INTO domain VALUES(2007,1001,'ham-n-eggs.tld');
INSERT INTO domain VALUES(2008,-2008,'orphan.tld');
INSERT INTO domain VALUES(2009,1003,'serverless.tld');
CREATE TABLE server_domain (
	server_id INTEGER NOT NULL, 
	domain_id INTEGER NOT NULL, 
	PRIMARY KEY (server_id, domain_id), 
	FOREIGN KEY(server_id) REFERENCES server (id), 
	FOREIGN KEY(domain_id) REFERENCES domain (id)
);
INSERT INTO server_domain VALUES(3000,2001);
INSERT INTO server_domain VALUES(3003,2001);
INSERT INTO server_domain VALUES(3004,2004);
INSERT INTO server_domain VALUES(3005,2004);
INSERT INTO server_domain VALUES(3004,2005);
INSERT INTO server_domain VALUES(3005,2005);
INSERT INTO server_domain VALUES(3009,2003);
INSERT INTO server_domain VALUES(3010,2003);
INSERT INTO server_domain VALUES(3006,2006);
INSERT INTO server_domain VALUES(3007,2006);
INSERT INTO server_domain VALUES(3000,2000);
INSERT INTO server_domain VALUES(3002,2000);
INSERT INTO server_domain VALUES(3001,2002);
INSERT INTO server_domain VALUES(3003,2002);
INSERT INTO server_domain VALUES(3008,2007);
COMMIT;
