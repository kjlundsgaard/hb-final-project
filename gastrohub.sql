--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.1
-- Dumped by pg_dump version 9.5.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: faves; Type: TABLE; Schema: public; Owner: KatieLundsgaard
--

CREATE TABLE faves (
    fave_id integer NOT NULL,
    restaurant_id integer,
    user_id integer
);


ALTER TABLE faves OWNER TO "KatieLundsgaard";

--
-- Name: faves_fave_id_seq; Type: SEQUENCE; Schema: public; Owner: KatieLundsgaard
--

CREATE SEQUENCE faves_fave_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE faves_fave_id_seq OWNER TO "KatieLundsgaard";

--
-- Name: faves_fave_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: KatieLundsgaard
--

ALTER SEQUENCE faves_fave_id_seq OWNED BY faves.fave_id;


--
-- Name: groups; Type: TABLE; Schema: public; Owner: KatieLundsgaard
--

CREATE TABLE groups (
    group_id integer NOT NULL,
    group_name character varying(100)
);


ALTER TABLE groups OWNER TO "KatieLundsgaard";

--
-- Name: groups_group_id_seq; Type: SEQUENCE; Schema: public; Owner: KatieLundsgaard
--

CREATE SEQUENCE groups_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE groups_group_id_seq OWNER TO "KatieLundsgaard";

--
-- Name: groups_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: KatieLundsgaard
--

ALTER SEQUENCE groups_group_id_seq OWNED BY groups.group_id;


--
-- Name: lists; Type: TABLE; Schema: public; Owner: KatieLundsgaard
--

CREATE TABLE lists (
    list_id integer NOT NULL,
    group_id integer,
    list_name character varying(100)
);


ALTER TABLE lists OWNER TO "KatieLundsgaard";

--
-- Name: lists_list_id_seq; Type: SEQUENCE; Schema: public; Owner: KatieLundsgaard
--

CREATE SEQUENCE lists_list_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE lists_list_id_seq OWNER TO "KatieLundsgaard";

--
-- Name: lists_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: KatieLundsgaard
--

ALTER SEQUENCE lists_list_id_seq OWNED BY lists.list_id;


--
-- Name: restaurants; Type: TABLE; Schema: public; Owner: KatieLundsgaard
--

CREATE TABLE restaurants (
    restaurant_id integer NOT NULL,
    restaurant_name character varying(100),
    yelp_rating double precision,
    latitude double precision,
    longitude double precision,
    address character varying(100),
    categories character varying(100),
    neighborhoods character varying(100),
    link character varying(200)
);


ALTER TABLE restaurants OWNER TO "KatieLundsgaard";

--
-- Name: restaurants_lists; Type: TABLE; Schema: public; Owner: KatieLundsgaard
--

CREATE TABLE restaurants_lists (
    restaurant_list_id integer NOT NULL,
    restaurant_id integer,
    list_id integer,
    visited boolean
);


ALTER TABLE restaurants_lists OWNER TO "KatieLundsgaard";

--
-- Name: restaurants_lists_restaurant_list_id_seq; Type: SEQUENCE; Schema: public; Owner: KatieLundsgaard
--

CREATE SEQUENCE restaurants_lists_restaurant_list_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE restaurants_lists_restaurant_list_id_seq OWNER TO "KatieLundsgaard";

--
-- Name: restaurants_lists_restaurant_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: KatieLundsgaard
--

ALTER SEQUENCE restaurants_lists_restaurant_list_id_seq OWNED BY restaurants_lists.restaurant_list_id;


--
-- Name: restaurants_restaurant_id_seq; Type: SEQUENCE; Schema: public; Owner: KatieLundsgaard
--

CREATE SEQUENCE restaurants_restaurant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE restaurants_restaurant_id_seq OWNER TO "KatieLundsgaard";

--
-- Name: restaurants_restaurant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: KatieLundsgaard
--

ALTER SEQUENCE restaurants_restaurant_id_seq OWNED BY restaurants.restaurant_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: KatieLundsgaard
--

CREATE TABLE users (
    user_id integer NOT NULL,
    email character varying(64),
    password character varying(64),
    fname character varying(20),
    lname character varying(20),
    salt character varying(50)
);


ALTER TABLE users OWNER TO "KatieLundsgaard";

--
-- Name: users_groups; Type: TABLE; Schema: public; Owner: KatieLundsgaard
--

CREATE TABLE users_groups (
    user_group_id integer NOT NULL,
    user_id integer,
    group_id integer
);


ALTER TABLE users_groups OWNER TO "KatieLundsgaard";

--
-- Name: users_groups_user_group_id_seq; Type: SEQUENCE; Schema: public; Owner: KatieLundsgaard
--

CREATE SEQUENCE users_groups_user_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_groups_user_group_id_seq OWNER TO "KatieLundsgaard";

--
-- Name: users_groups_user_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: KatieLundsgaard
--

ALTER SEQUENCE users_groups_user_group_id_seq OWNED BY users_groups.user_group_id;


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: KatieLundsgaard
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO "KatieLundsgaard";

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: KatieLundsgaard
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: fave_id; Type: DEFAULT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY faves ALTER COLUMN fave_id SET DEFAULT nextval('faves_fave_id_seq'::regclass);


--
-- Name: group_id; Type: DEFAULT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY groups ALTER COLUMN group_id SET DEFAULT nextval('groups_group_id_seq'::regclass);


--
-- Name: list_id; Type: DEFAULT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY lists ALTER COLUMN list_id SET DEFAULT nextval('lists_list_id_seq'::regclass);


--
-- Name: restaurant_id; Type: DEFAULT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY restaurants ALTER COLUMN restaurant_id SET DEFAULT nextval('restaurants_restaurant_id_seq'::regclass);


--
-- Name: restaurant_list_id; Type: DEFAULT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY restaurants_lists ALTER COLUMN restaurant_list_id SET DEFAULT nextval('restaurants_lists_restaurant_list_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Name: user_group_id; Type: DEFAULT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY users_groups ALTER COLUMN user_group_id SET DEFAULT nextval('users_groups_user_group_id_seq'::regclass);


--
-- Data for Name: faves; Type: TABLE DATA; Schema: public; Owner: KatieLundsgaard
--

COPY faves (fave_id, restaurant_id, user_id) FROM stdin;
1	1	1
2	2	1
3	8	1
4	9	1
5	14	1
6	18	1
7	25	1
\.


--
-- Name: faves_fave_id_seq; Type: SEQUENCE SET; Schema: public; Owner: KatieLundsgaard
--

SELECT pg_catalog.setval('faves_fave_id_seq', 7, true);


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: KatieLundsgaard
--

COPY groups (group_id, group_name) FROM stdin;
1	Just for Me
2	Family
3	Roomies
4	NYC Friends
5	Significant Other
\.


--
-- Name: groups_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: KatieLundsgaard
--

SELECT pg_catalog.setval('groups_group_id_seq', 5, true);


--
-- Data for Name: lists; Type: TABLE DATA; Schema: public; Owner: KatieLundsgaard
--

COPY lists (list_id, group_id, list_name) FROM stdin;
1	2	Raleigh/Durham Restaurants
2	2	Milwaukee Restaurants
3	3	Sports Bars
4	1	Taquerias
5	1	Pizza Places
6	4	NYC Brunch
7	4	NYC Bars
8	5	Date Spots
\.


--
-- Name: lists_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: KatieLundsgaard
--

SELECT pg_catalog.setval('lists_list_id_seq', 8, true);


--
-- Data for Name: restaurants; Type: TABLE DATA; Schema: public; Owner: KatieLundsgaard
--

COPY restaurants (restaurant_id, restaurant_name, yelp_rating, latitude, longitude, address, categories, neighborhoods, link) FROM stdin;
1	La Taqueria	4	37.7508830000000017	-122.418122999999994	2889 Mission St	Mexican,mexican	Mission	http://www.yelp.com/biz/la-taqueria-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
2	El Farolito	4	37.7526539999999997	-122.418191500000006	2779 Mission St	Mexican,mexican	Mission	http://www.yelp.com/biz/el-farolito-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
3	Taqueria Guadalajara	4.5	37.7212907373904969	-122.437459006905996	4798 Mission St	Mexican,mexican	Excelsior,Outer Mission,Mission Terrace	http://www.yelp.com/biz/taqueria-guadalajara-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
4	Taqueria Cancún	4	37.760469999999998	-122.419510000000002	2288 Mission St	Mexican,mexican	Mission	http://www.yelp.com/biz/taqueria-canc%C3%BAn-san-francisco-5?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
5	El Castillito	4	37.7688743812287981	-122.429237365722997	136 Church St	Mexican,mexican	Duboce Triangle	http://www.yelp.com/biz/el-castillito-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
6	Mateo's Taqueria	4.5	37.7575399999999988	-122.418760000000006	2471 Mission St	Mexican,mexican,Breakfast & Brunch,breakfast_brunch,Vegetarian,vegetarian	Mission	http://www.yelp.com/biz/mateos-taqueria-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
7	Gordo Taqueria	4	37.7823199999999986	-122.483639999999994	2252 Clement St	Fast Food,hotdogs,Mexican,mexican	Outer Richmond	http://www.yelp.com/biz/gordo-taqueria-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
8	The Little Chihuahua	4	37.7720399000000029	-122.436880000000002	292 Divisadero St	Mexican,mexican	Lower Haight	http://www.yelp.com/biz/the-little-chihuahua-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
9	Little Star Pizza	4.5	37.7775382995604971	-122.43798828125	846 Divisadero St	Pizza,pizza	Alamo Square	http://www.yelp.com/biz/little-star-pizza-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
10	Pizzeria Delfina	4	37.7613600000000034	-122.424180000000007	3611 18th St	Pizza,pizza,Italian,italian	Mission	http://www.yelp.com/biz/pizzeria-delfina-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
11	Escape From New York Pizza	4	37.7694455999999974	-122.451272200000005	1737 Haight St	Pizza,pizza	The Haight	http://www.yelp.com/biz/escape-from-new-york-pizza-san-francisco-3?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
12	Marcello's Pizza	4	37.7620544433594034	-122.435386657715	420 Castro St	Pizza,pizza	Castro	http://www.yelp.com/biz/marcellos-pizza-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
13	Humble Pie	4	35.7763169999999988	-78.6449750000000023	317 S Harrington St	Breakfast & Brunch,breakfast_brunch,American (New),newamerican,Bars,bars		http://www.yelp.com/biz/humble-pie-raleigh?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
14	Trophy Brewing Company	4	35.779844149947202	-78.6535571515560008	827 W Morgan St	Bars,bars,Breweries,breweries,Pizza,pizza		http://www.yelp.com/biz/trophy-brewing-company-raleigh?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
15	David's Dumpling & Noodle Bar	4	35.7859880000000032	-78.6616060000000061	1900 Hillsborough St	Asian Fusion,asianfusion,Chinese,chinese		http://www.yelp.com/biz/davids-dumpling-and-noodle-bar-raleigh?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
16	Beasley's Chicken & Honey	4	35.7769680003969981	-78.638127588482007	237 S Wilmington St	Southern,southern,American (New),newamerican		http://www.yelp.com/biz/beasleys-chicken-and-honey-raleigh?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
17	Second Empire Restaurant	4.5	35.780738999999997	-78.6448230000000024	330 Hillsborough St	American (New),newamerican		http://www.yelp.com/biz/second-empire-restaurant-and-tavern-raleigh?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
18	Odd Duck	4.5	43.0020580440760014	-87.9034519940614985	2352 S Kinnickinnic Ave	American (New),newamerican,Vegetarian,vegetarian,Tapas/Small Plates,tapasmallplates	Bay View	http://www.yelp.com/biz/odd-duck-milwaukee?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
19	Drink Wisconsinbly Pub	4	43.023069999999997	-87.9101500000000016	135 E National Ave	Bars,bars,American (Traditional),tradamerican	Walker's Point	http://www.yelp.com/biz/drink-wisconsinbly-pub-milwaukee-2?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
20	Oscar's Pub & Grill	4.5	43.0245590000000036	-87.9347992000000005	1712 W Pierce St	American (New),newamerican,Pubs,pubs,Burgers,burgers	Mitchell Park	http://www.yelp.com/biz/oscars-pub-and-grill-milwaukee?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
21	Swingin' Door Exchange	4.5	43.0372911999999985	-87.9081814000000037	219 E Michigan St	Bars,bars,American (New),newamerican	East Town,Downtown	http://www.yelp.com/biz/swingin-door-exchange-milwaukee?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
22	Über Tap Room and Cheese Bar	4.5	43.0441467781380993	-87.914271354675293	1048 N. Old World 3rd St	Gastropubs,gastropubs	Westown	http://www.yelp.com/biz/%C3%BCber-tap-room-and-cheese-bar-milwaukee?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
23	Nickies	4	37.7723999999999975	-122.429850000000002	466 Haight St	Sports Bars,sportsbars,American (New),newamerican	Lower Haight,Hayes Valley	http://www.yelp.com/biz/nickies-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
24	Kezar Pub	4	37.7678833007812003	-122.452903747559006	770 Stanyan St	Pubs,pubs,Sports Bars,sportsbars,American (Traditional),tradamerican	Cole Valley	http://www.yelp.com/biz/kezar-pub-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
25	Hi Tops	4	37.7650073915719986	-122.431905493139993	2247 Market St	Sports Bars,sportsbars,American (New),newamerican,Gay Bars,gaybars	Castro	http://www.yelp.com/biz/hi-tops-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
26	Danny Coyle's	4	37.7719359641183985	-122.433228492737001	668 Haight St	Pubs,pubs,Sports Bars,sportsbars	Lower Haight	http://www.yelp.com/biz/danny-coyles-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
27	Le Barricou	4	40.711190000000002	-73.9500400000000013	533 Grand St	Breakfast & Brunch,breakfast_brunch,French,french	Williamsburg - North Side	http://www.yelp.com/biz/le-barricou-brooklyn?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
28	Black Cat LES	4	40.7191290000000023	-73.9845090000000027	172 Rivington St	Coffee & Tea,coffee,Breakfast & Brunch,breakfast_brunch	Lower East Side	http://www.yelp.com/biz/black-cat-les-new-york-2?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
29	Les Enfants de Boheme	4.5	40.713539645075798	-73.9887866377830932	177 Henry St	French,french,Cafes,cafes,Cocktail Bars,cocktailbars	Two Bridges,Lower East Side	http://www.yelp.com/biz/les-enfants-de-boheme-new-york?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
30	Clinton Street Baking Company	4	40.7211280000000002	-73.9839329999999933	4 Clinton St	Breakfast & Brunch,breakfast_brunch	Lower East Side	http://www.yelp.com/biz/clinton-street-baking-company-new-york-4?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
31	Dromedary Bar	4.5	40.6995769999999979	-73.9158630000000016	266 irving ave.	Cocktail Bars,cocktailbars,American (New),newamerican	Bushwick	http://www.yelp.com/biz/dromedary-bar-brooklyn?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
32	Sycamore	4	40.639663696289098	-73.9671859741210938	1118 Cortelyou Rd	Bars,bars,Florists,florists,Music Venues,musicvenues	Flatbush	http://www.yelp.com/biz/sycamore-brooklyn-2?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
33	Brooklyn Ice House	4.5	40.6791899999999984	-74.0110990000000015	318 Van Brunt St	Barbeque,bbq,Pubs,pubs	Red Hook	http://www.yelp.com/biz/brooklyn-ice-house-brooklyn?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
34	The Adirondack	4.5	40.6525200000000027	-73.9758388999999994	1241A Prospect Ave	Bars,bars	Windsor Terrace	http://www.yelp.com/biz/the-adirondack-brooklyn?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
35	Maven	4	37.7722329999999999	-122.432006999999999	598 Haight St	American (New),newamerican,Gastropubs,gastropubs,Cocktail Bars,cocktailbars	Lower Haight	http://www.yelp.com/biz/maven-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
36	Nopa	4	37.774883043712002	-122.437558482219998	560 Divisadero St	American (New),newamerican,Modern European,modern_european	Alamo Square	http://www.yelp.com/biz/nopa-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
37	Bean Bag Cafe	4	37.7750101000000029	-122.437842099999997	601 Divisadero St	Coffee & Tea,coffee,Burgers,burgers,Sandwiches,sandwiches	NoPa,Alamo Square	http://www.yelp.com/biz/bean-bag-cafe-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
38	Domo	4	37.7758600000000015	-122.426310000000001	511 Laguna St	Sushi Bars,sushi,Japanese,japanese	Hayes Valley	http://www.yelp.com/biz/domo-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
39	Fly Bar	4	37.7767499999999998	-122.437849999999997	762 Divisadero St	Bars,bars,American (Traditional),tradamerican	Alamo Square	http://www.yelp.com/biz/fly-bar-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
40	Wine Kitchen	4	37.7743492126464986	-122.437995910645	507 Divisadero St	Tapas/Small Plates,tapasmallplates,Wine Bars,wine_bars,American (New),newamerican	NoPa	http://www.yelp.com/biz/wine-kitchen-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
41	Alamo Square Seafood Grill	4	37.7770569535080014	-122.431621310530005	803 Fillmore St	Seafood,seafood	Alamo Square	http://www.yelp.com/biz/alamo-square-seafood-grill-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=HO0z7lMZLyUjzzoxIhGVHw
\.


--
-- Data for Name: restaurants_lists; Type: TABLE DATA; Schema: public; Owner: KatieLundsgaard
--

COPY restaurants_lists (restaurant_list_id, restaurant_id, list_id, visited) FROM stdin;
6	6	4	f
1	1	4	t
2	2	4	t
3	3	4	t
4	4	4	t
5	5	4	t
7	7	4	t
8	8	4	t
10	10	5	f
12	12	5	f
9	9	5	t
11	11	5	t
15	15	1	f
16	16	1	f
17	17	1	f
13	13	1	t
14	14	1	t
18	18	2	t
19	19	2	f
20	20	2	f
21	21	2	f
22	22	2	f
23	23	3	f
24	24	3	f
25	25	3	t
26	26	3	t
27	27	6	f
28	28	6	f
29	29	6	f
30	30	6	f
31	31	7	f
32	32	7	f
33	33	7	f
34	34	7	f
35	35	8	f
36	36	8	t
38	38	8	f
40	40	8	f
41	41	8	f
39	39	8	t
37	37	8	t
\.


--
-- Name: restaurants_lists_restaurant_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: KatieLundsgaard
--

SELECT pg_catalog.setval('restaurants_lists_restaurant_list_id_seq', 41, true);


--
-- Name: restaurants_restaurant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: KatieLundsgaard
--

SELECT pg_catalog.setval('restaurants_restaurant_id_seq', 41, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: KatieLundsgaard
--

COPY users (user_id, email, password, fname, lname, salt) FROM stdin;
1	katie.lundsgaard@gmail.com	$2b$12$M4qI.KAbDZGdgYbmEQ2iQOsxng.qU.LMExo/UDTOM3MWjz9vzvhwO	Katie	Lundsgaard	$2b$12$M4qI.KAbDZGdgYbmEQ2iQO
2	ilana@gmail.com	$2b$12$lBlXIPzAVqJ4AtuuUeU5VeBKN5.hfDykwqsYF7n8Clti8GmLVkc7O	Ilana	Glazer	$2b$12$lBlXIPzAVqJ4AtuuUeU5Ve
3	abby@gmail.com	$2b$12$n1LBLty8DggXoOazJtag6uQtvkTbzbPkNXyO0UkE6aTUZGV4RR.zm	Abby	Jacobson	$2b$12$n1LBLty8DggXoOazJtag6u
4	kaj@gmail.com	$2b$12$uHRzizg/xg6dvAxqf9fRfeMaNULtyKBYXueuGKjGFKu9C4fjC59rC	Kaj	Lundsgaard	$2b$12$uHRzizg/xg6dvAxqf9fRfe
5	maggie@gmail.com	$2b$12$TXvtpvwrSQa1l.T8wr3kJudsb.qhonTWHtKN6j.QsocW6YhaWav4i	Maggie	Lundsgaard	$2b$12$TXvtpvwrSQa1l.T8wr3kJu
6	niels@gmail.com	$2b$12$e/l56MJD3ibKb3ERxty0fuAQqtZDF0BYDfGFzaVhkzsBcYlLwRj9a	Niels	Lundsgaard	$2b$12$e/l56MJD3ibKb3ERxty0fu
7	jane@gmail.com	$2b$12$79zrU3v2rnI61e/RW3n9OeAKMz46c9/DDmsLkuRRxUPJ.1QjhG1AK	Jane	Lundsgaard	$2b$12$79zrU3v2rnI61e/RW3n9Oe
8	bengoldstein@gmail.com	$2b$12$QzHvNt4UPRLEyCUUfdvfw.sLsQ0cUbZaeP0c/jF9K/hEE9WCxF2iS	Ben	Goldstein	$2b$12$QzHvNt4UPRLEyCUUfdvfw.
9	benlevine@gmail.com	$2b$12$6qLwy7R9aUh7P3cHPVLu/uaq41cxGg1WlRBFiYaM8lhLM.8mdf7hm	Ben	Levine	$2b$12$6qLwy7R9aUh7P3cHPVLu/u
10	theo@gmail.com	$2b$12$cBRKz5uhc41DtQ5QaBE2QudTPuy.M/KcI0dcngpNjtVnbfZFIDCCO	Theo	Hopkinson	$2b$12$cBRKz5uhc41DtQ5QaBE2Qu
11	justine@gmail.com	$2b$12$D2rK0c7Ip.BqR0xRck0YZ.jOIvGmSTXO1m1goMOxd7GriRv/mFaSu	Justine	Selsing	$2b$12$D2rK0c7Ip.BqR0xRck0YZ.
12	toni@gmail.com	$2b$12$C8xLLj5gvrVvNlhWmSN41ubY2DU9JVaSUh3cbk/lBx0kagdSLwEAu	Toni	DaCosta	$2b$12$C8xLLj5gvrVvNlhWmSN41u
13	lauren@gmail.com	$2b$12$Nu.vzMqRuoAi/od9QU65ZuS3HtEDrhTUDZC4SwDpJZqnxlQRMoize	Lauren	Gaffney	$2b$12$Nu.vzMqRuoAi/od9QU65Zu
14	colin@gmail.com	$2b$12$5O/t7Eoj174rfuB9nlSTa.PGSGT/NbDEqvOXmr/IFFPsQ2iToV5xa	Colin	Holtzinger	$2b$12$5O/t7Eoj174rfuB9nlSTa.
15	abbi@gmail.com	$2b$12$BPBKadM2pcnKoAxqwmg5LedMQPLnXxVTJSEJsySv/AQqoIfou6E0q	Abbi	Jacobson	$2b$12$BPBKadM2pcnKoAxqwmg5Le
16	jenny@gmail.com	$2b$12$zpDMtPcwbDOwNTjuDhXgYeyPjhmitl4H50dEd/NoWHzh7h/h/v9sa	Jenny	Kreizman	$2b$12$zpDMtPcwbDOwNTjuDhXgYe
17	sarah@gmail.com	$2b$12$yt8AvGLOFKV/mAPRqI7UpuVdN2Bte/3qdhCDYOneYLD2EkkqpEF.y	Sarah	Stroud	$2b$12$yt8AvGLOFKV/mAPRqI7Upu
18	kevin@gmail.com	$2b$12$Be3frWgYTJp58TJEGsqJqOPpVODL9K0KNx7..j4yF5gC/xjXeaSwq	Kevin	Munger	$2b$12$Be3frWgYTJp58TJEGsqJqO
\.


--
-- Data for Name: users_groups; Type: TABLE DATA; Schema: public; Owner: KatieLundsgaard
--

COPY users_groups (user_group_id, user_id, group_id) FROM stdin;
1	1	1
2	1	2
3	1	3
4	1	4
5	1	5
6	4	2
7	5	2
8	6	2
9	7	2
10	9	3
11	10	3
12	14	3
13	12	3
14	11	3
15	13	3
16	8	5
17	17	4
18	18	4
19	16	4
20	15	4
21	2	4
\.


--
-- Name: users_groups_user_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: KatieLundsgaard
--

SELECT pg_catalog.setval('users_groups_user_group_id_seq', 21, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: KatieLundsgaard
--

SELECT pg_catalog.setval('users_user_id_seq', 18, true);


--
-- Name: faves_pkey; Type: CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY faves
    ADD CONSTRAINT faves_pkey PRIMARY KEY (fave_id);


--
-- Name: groups_pkey; Type: CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (group_id);


--
-- Name: lists_pkey; Type: CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY lists
    ADD CONSTRAINT lists_pkey PRIMARY KEY (list_id);


--
-- Name: restaurants_lists_pkey; Type: CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY restaurants_lists
    ADD CONSTRAINT restaurants_lists_pkey PRIMARY KEY (restaurant_list_id);


--
-- Name: restaurants_pkey; Type: CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY restaurants
    ADD CONSTRAINT restaurants_pkey PRIMARY KEY (restaurant_id);


--
-- Name: users_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY users_groups
    ADD CONSTRAINT users_groups_pkey PRIMARY KEY (user_group_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: faves_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY faves
    ADD CONSTRAINT faves_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id);


--
-- Name: faves_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY faves
    ADD CONSTRAINT faves_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: lists_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY lists
    ADD CONSTRAINT lists_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(group_id);


--
-- Name: restaurants_lists_list_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY restaurants_lists
    ADD CONSTRAINT restaurants_lists_list_id_fkey FOREIGN KEY (list_id) REFERENCES lists(list_id);


--
-- Name: restaurants_lists_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY restaurants_lists
    ADD CONSTRAINT restaurants_lists_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id);


--
-- Name: users_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY users_groups
    ADD CONSTRAINT users_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(group_id);


--
-- Name: users_groups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: KatieLundsgaard
--

ALTER TABLE ONLY users_groups
    ADD CONSTRAINT users_groups_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

