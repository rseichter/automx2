--
-- PostgreSQL database dump
--

-- Dumped from database version 14.0 (Debian 14.0-1.pgdg110+1)
-- Dumped by pg_dump version 14.0 (Debian 14.0-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: davserver; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.davserver (
    id integer NOT NULL,
    url character varying(128) NOT NULL,
    port integer NOT NULL,
    type character varying(32) NOT NULL,
    use_ssl boolean NOT NULL,
    domain_required boolean NOT NULL,
    user_name character varying(64)
);


ALTER TABLE public.davserver OWNER TO "user";

--
-- Name: davserver_domain; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.davserver_domain (
    davserver_id integer NOT NULL,
    domain_id integer NOT NULL
);


ALTER TABLE public.davserver_domain OWNER TO "user";

--
-- Name: davserver_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.davserver_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.davserver_id_seq OWNER TO "user";

--
-- Name: davserver_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.davserver_id_seq OWNED BY public.davserver.id;


--
-- Name: domain; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.domain (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    provider_id integer NOT NULL,
    ldapserver_id integer
);


ALTER TABLE public.domain OWNER TO "user";

--
-- Name: domain_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.domain_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.domain_id_seq OWNER TO "user";

--
-- Name: domain_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.domain_id_seq OWNED BY public.domain.id;


--
-- Name: ldapserver; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.ldapserver (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    port integer NOT NULL,
    use_ssl boolean NOT NULL,
    search_base character varying(128) NOT NULL,
    search_filter character varying(128) NOT NULL,
    attr_uid character varying(32) NOT NULL,
    attr_cn character varying(32),
    bind_password character varying(128),
    bind_user character varying(128)
);


ALTER TABLE public.ldapserver OWNER TO "user";

--
-- Name: ldapserver_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.ldapserver_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ldapserver_id_seq OWNER TO "user";

--
-- Name: ldapserver_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.ldapserver_id_seq OWNED BY public.ldapserver.id;


--
-- Name: provider; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.provider (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    short_name character varying(32) NOT NULL,
	sign boolean DEFAULT 0 NOT NULL,
	sign_cert text null,
	sign_key text null
);


ALTER TABLE public.provider OWNER TO "user";

--
-- Name: provider_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.provider_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.provider_id_seq OWNER TO "user";

--
-- Name: provider_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.provider_id_seq OWNED BY public.provider.id;


--
-- Name: server; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.server (
    id integer NOT NULL,
    prio integer DEFAULT 10 NOT NULL,
    name character varying(128) NOT NULL,
    port integer NOT NULL,
    type character varying(32) NOT NULL,
    socket_type character varying(32) NOT NULL,
    user_name character varying(64) NOT NULL,
    authentication character varying(32) NOT NULL
);


ALTER TABLE public.server OWNER TO "user";

--
-- Name: server_domain; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.server_domain (
    server_id integer NOT NULL,
    domain_id integer NOT NULL
);


ALTER TABLE public.server_domain OWNER TO "user";

--
-- Name: server_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.server_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.server_id_seq OWNER TO "user";

--
-- Name: server_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.server_id_seq OWNED BY public.server.id;


--
-- Name: davserver id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.davserver ALTER COLUMN id SET DEFAULT nextval('public.davserver_id_seq'::regclass);


--
-- Name: domain id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.domain ALTER COLUMN id SET DEFAULT nextval('public.domain_id_seq'::regclass);


--
-- Name: ldapserver id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.ldapserver ALTER COLUMN id SET DEFAULT nextval('public.ldapserver_id_seq'::regclass);


--
-- Name: provider id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.provider ALTER COLUMN id SET DEFAULT nextval('public.provider_id_seq'::regclass);


--
-- Name: server id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.server ALTER COLUMN id SET DEFAULT nextval('public.server_id_seq'::regclass);


--
-- Name: davserver_domain davserver_domain_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.davserver_domain
    ADD CONSTRAINT davserver_domain_pkey PRIMARY KEY (davserver_id, domain_id);


--
-- Name: davserver davserver_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.davserver
    ADD CONSTRAINT davserver_pkey PRIMARY KEY (id);


--
-- Name: domain domain_name_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.domain
    ADD CONSTRAINT domain_name_key UNIQUE (name);


--
-- Name: domain domain_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.domain
    ADD CONSTRAINT domain_pkey PRIMARY KEY (id);


--
-- Name: ldapserver ldapserver_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.ldapserver
    ADD CONSTRAINT ldapserver_pkey PRIMARY KEY (id);


--
-- Name: provider provider_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.provider
    ADD CONSTRAINT provider_pkey PRIMARY KEY (id);


--
-- Name: server_domain server_domain_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.server_domain
    ADD CONSTRAINT server_domain_pkey PRIMARY KEY (server_id, domain_id);


--
-- Name: server server_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.server
    ADD CONSTRAINT server_pkey PRIMARY KEY (id);


--
-- Name: davserver_domain davserver_domain_davserver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.davserver_domain
    ADD CONSTRAINT davserver_domain_davserver_id_fkey FOREIGN KEY (davserver_id) REFERENCES public.davserver(id);


--
-- Name: davserver_domain davserver_domain_domain_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.davserver_domain
    ADD CONSTRAINT davserver_domain_domain_id_fkey FOREIGN KEY (domain_id) REFERENCES public.domain(id);


--
-- Name: domain domain_ldapserver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.domain
    ADD CONSTRAINT domain_ldapserver_id_fkey FOREIGN KEY (ldapserver_id) REFERENCES public.ldapserver(id);


--
-- Name: domain domain_provider_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.domain
    ADD CONSTRAINT domain_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES public.provider(id);


--
-- Name: server_domain server_domain_domain_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.server_domain
    ADD CONSTRAINT server_domain_domain_id_fkey FOREIGN KEY (domain_id) REFERENCES public.domain(id);


--
-- Name: server_domain server_domain_server_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.server_domain
    ADD CONSTRAINT server_domain_server_id_fkey FOREIGN KEY (server_id) REFERENCES public.server(id);


--
-- PostgreSQL database dump complete
--

