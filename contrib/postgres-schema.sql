-- PostgreSQL 13.2 (Debian 13.2-1.pgdg100+1) dump

CREATE TABLE "public"."alembic_version" (
  "version_num" character varying(32) NOT NULL,
  CONSTRAINT "alembic_version_pkc" PRIMARY KEY ("version_num")
) WITH (oids = false);

INSERT INTO "alembic_version" ("version_num") VALUES
('5334f8a8282c');


CREATE SEQUENCE domain_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."domain" (
  "id" integer DEFAULT nextval('domain_id_seq') NOT NULL,
  "name" character varying(128) NOT NULL,
  "provider_id" integer NOT NULL,
  "ldapserver_id" integer,
  CONSTRAINT "domain_name_key" UNIQUE ("name"),
  CONSTRAINT "domain_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "domain" ("id", "name", "provider_id", "ldapserver_id") VALUES
(1, 'example.com', 1, NULL);


CREATE SEQUENCE ldapserver_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."ldapserver" (
  "id" integer DEFAULT nextval('ldapserver_id_seq') NOT NULL,
  "name" character varying(128) NOT NULL,
  "port" integer NOT NULL,
  "use_ssl" boolean NOT NULL,
  "search_base" character varying(128) NOT NULL,
  "search_filter" character varying(128) NOT NULL,
  "attr_uid" character varying(128) NOT NULL,
  "attr_cn" character varying(128),
  "bind_password" character varying(128),
  "bind_user" character varying(128),
  CONSTRAINT "ldapserver_pkey" PRIMARY KEY ("id")
) WITH (oids = false);



CREATE SEQUENCE provider_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."provider" (
  "id" integer DEFAULT nextval('provider_id_seq') NOT NULL,
  "name" character varying(128) NOT NULL,
  "short_name" character varying(128) NOT NULL,
  CONSTRAINT "provider_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "provider" ("id", "name", "short_name") VALUES
(1, 'Example Inc.', 'Example');


CREATE SEQUENCE server_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 2 CACHE 1;

CREATE TABLE "public"."server" (
  "id" integer DEFAULT nextval('server_id_seq') NOT NULL,
  "name" character varying(128) NOT NULL,
  "port" integer NOT NULL,
  "type" character varying(128) NOT NULL,
  "socket_type" character varying(128) NOT NULL,
  "user_name" character varying(128) NOT NULL,
  "authentication" character varying(128) NOT NULL,
  "prio" integer DEFAULT '10' NOT NULL,
  CONSTRAINT "server_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "server" ("id", "name", "port", "type", "socket_type", "user_name", "authentication", "prio") VALUES
(1, 'imap.example.com', 993, 'imap', 'SSL', '%EMAILADDRESS%', 'plain', 10),
(2, 'smtp.example.com', 587, 'smtp', 'STARTTLS', '%EMAILADDRESS%', 'plain', 10);


CREATE TABLE "public"."server_domain" (
  "server_id" integer NOT NULL,
  "domain_id" integer NOT NULL,
  CONSTRAINT "server_domain_pkey" PRIMARY KEY ("server_id", "domain_id")
) WITH (oids = false);

INSERT INTO "server_domain" ("server_id", "domain_id") VALUES
(1, 1),
(2, 1);

ALTER TABLE ONLY "public"."domain" ADD CONSTRAINT "domain_ldapserver_id_fkey" FOREIGN KEY (ldapserver_id) REFERENCES ldapserver(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."domain" ADD CONSTRAINT "domain_provider_id_fkey" FOREIGN KEY (provider_id) REFERENCES provider(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."server_domain" ADD CONSTRAINT "server_domain_domain_id_fkey" FOREIGN KEY (domain_id) REFERENCES domain(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."server_domain" ADD CONSTRAINT "server_domain_server_id_fkey" FOREIGN KEY (server_id) REFERENCES server(id) NOT DEFERRABLE;
