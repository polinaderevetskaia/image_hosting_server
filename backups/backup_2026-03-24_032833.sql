--
-- PostgreSQL database dump
--

\restrict XuC893alSMar8rtkUlMHl0RKDQX6YFONnayqWPMZQqCkiv3RgErLp12pv5W7JhN

-- Dumped from database version 15.17 (Debian 15.17-1.pgdg13+1)
-- Dumped by pg_dump version 15.17 (Debian 15.17-1.pgdg13+1)

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
-- Name: images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.images (
    id integer NOT NULL,
    filename text NOT NULL,
    original_name text NOT NULL,
    size integer NOT NULL,
    file_type text NOT NULL,
    upload_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.images OWNER TO postgres;

--
-- Name: images_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.images_id_seq OWNER TO postgres;

--
-- Name: images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.images_id_seq OWNED BY public.images.id;


--
-- Name: images id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images ALTER COLUMN id SET DEFAULT nextval('public.images_id_seq'::regclass);


--
-- Data for Name: images; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.images (id, filename, original_name, size, file_type, upload_time) FROM stdin;
1	4d24064c-6346-4f76-849c-d8c0a90d9ec5.jpeg	4k.jpeg	9326	jpeg	2026-03-24 01:18:35.620955
2	7c10fbb8-641c-4297-ae11-45964a28e0cc.jpeg	Без названия.jpeg	5986	jpeg	2026-03-24 01:19:00.404276
3	ea54ae83-ff40-4a73-b3d4-750632201e1f.jpeg	nature.jpeg	9225	jpeg	2026-03-24 01:19:14.867205
4	de01622c-f46f-486e-aaf9-488cdb41cc10.jpeg	nature2.jpeg	8636	jpeg	2026-03-24 01:19:14.871283
5	160df32d-79b1-4568-824f-f5292905a150.jpeg	nature3.jpeg	16139	jpeg	2026-03-24 01:19:14.879138
\.


--
-- Name: images_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.images_id_seq', 5, true);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict XuC893alSMar8rtkUlMHl0RKDQX6YFONnayqWPMZQqCkiv3RgErLp12pv5W7JhN

