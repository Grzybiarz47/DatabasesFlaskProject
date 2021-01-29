CREATE OR REPLACE FUNCTION projekt."dodaj_artystę" (
  text,
  text,
  integer = '-1'::integer,
  integer = '-1'::integer
)
RETURNS integer AS
$body$
DECLARE
	id integer;
    q text;
BEGIN
    if(SELECT COUNT(projekt.id_artysty($1, $2)) = 1) then
    	id := (SELECT projekt.id_artysty($1, $2))::integer;
        q := 'UPDATE "projekt"."ARTYSTA" SET';
        q := q || ' imie = '''|| $1 || ''', nazwisko = ''' || $2 || ''', data_urodzenia = ' || $3 || ', data_smierci = ' || $4;
        q := q || ' WHERE id_artysta = ' || id;
        EXECUTE 'DELETE FROM "projekt"."RODZAJ_ARTYSTY" WHERE id_artysta = ' || id;
    else
    	id := (SELECT projekt.next_id('ARTYSTA', 'id_artysta'));
    	q := 'INSERT INTO "projekt"."ARTYSTA" (id_artysta, imie, nazwisko, data_urodzenia, data_smierci) VALUES ';
        q := q || '(' || id || ', ''' || $1 || ''', ''' || $2 || ''', ' || $3 || ', ' ||$4 || ')';
    end if;
    EXECUTE q;
    return id;
END;
$body$
LANGUAGE 'plpgsql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.dodaj_film (
  text,
  text,
  text,
  text,
  integer = '-1'::integer
)
RETURNS integer AS
$body$
INSERT INTO "projekt"."FILM" (id_film, nazwa, opis, box_office, studio, rok_produkcji) VALUES
(projekt.next_id('FILM', 'id_film'), $1, $2, $3, $4, $5) RETURNING id_film
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt."dodaj_grę" (
  text,
  text,
  text,
  text,
  integer = '-1'::integer
)
RETURNS integer AS
$body$
INSERT INTO "projekt"."GRA" (id_gra, nazwa, opis, sprzedaz, studio, rok_produkcji) VALUES
(projekt.next_id('GRA', 'id_gra'), $1, $2, $3, $4, $5) RETURNING id_gra
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt."dodaj_nagrodę" (
  name varchar,
  year integer = NULL::integer,
  name_movie varchar = NULL::character varying,
  name_series varchar = NULL::character varying,
  name_game varchar = NULL::character varying,
  fname_artist varchar = NULL::character varying,
  lname_artist varchar = NULL::character varying
)
RETURNS boolean AS
$body$
DECLARE
	id_serial integer;
    id_film integer;
    id_gra integer;
    id_artysta integer;
    q text;
    vals text;
    finalq text;
BEGIN
	q := 'INSERT INTO "projekt"."NAGRODA" (';
    vals := 'VALUES (';
    if(SELECT COUNT(projekt.id_filmu(name_movie)) = 1) then
    	id_film := (SELECT projekt.id_filmu(name_movie))::integer;
        q := q || 'id_film' || ', ';
        vals := vals || id_film || ', ';
    else
    	id_film = NULL;
    end if;
    
	if(SELECT COUNT(projekt.id_serialu(name_series)) = 1) then
    	id_serial := (SELECT projekt.id_serialu(name_series))::integer;
        q := q || 'id_serial' || ', ';
        vals := vals || id_serial || ', ';
    else
    	id_serial := NULL;
    end if;

    if(SELECT COUNT(projekt.id_gry(name_game)) = 1) then
    	id_gra := (SELECT projekt.id_gry(name_game))::integer;
        q := q || 'id_gra' || ', ';
        vals := vals || id_gra || ', ';
    else
    	id_gra := NULL;
    end if;
    
    if(SELECT COUNT(projekt.id_artysty(fname_artist, lname_artist)) = 1) then
    	id_artysta := (SELECT projekt.id_artysty(fname_artist, lname_artist))::integer;
    	q := q || 'id_artysta' || ', ';
        vals := vals || id_artysta || ', ';
    else
    	id_artysta := NULL;
    end if;
    
    q := q || 'rok_przyznania' || ', ' || 'nazwa) ';
    vals := vals || year || ', ''' || name || ''')';
    finalq := q || vals;
    
    if(id_artysta IS NOT NULL or id_film IS NOT NULL or id_serial IS NOT NULL or id_gra IS NOT NULL) then
    	EXECUTE finalq;
        return true;
    end if;
    return false;
END;
$body$
LANGUAGE 'plpgsql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt."dodaj_obsadę" (
  name_ms varchar,
  role_ms varchar,
  character_ms varchar,
  id_artist integer
)
RETURNS boolean AS
$body$
DECLARE
	id_serial integer;
    id_film integer;
    q text;
BEGIN
	if(SELECT COUNT(projekt.id_filmu(name_ms)) = 1) then
    	id_film = (SELECT (projekt.id_filmu(name_ms)));
        q := 'INSERT INTO "projekt"."ARTYSTA_FILM" (id_artysta, id_film, rola, postac) VALUES';
        q := q || '(' || id_artist || ', ' || id_film || ', ''' || role_ms || ''', ''' || character_ms || ''')';
        EXECUTE q;
        return true;
    elsif (SELECT COUNT(projekt.id_serialu(name_ms)) = 1) then
    	id_serial = (SELECT (projekt.id_serialu(name_ms)));
        q := 'INSERT INTO "projekt"."ARTYSTA_SERIAL" (id_artysta, id_serial, rola, postac) VALUES';
        q := q || '(' || id_artist || ', ' || id_serial || ', ''' || role_ms || ''', ''' || character_ms || ''')';
        EXECUTE q;
        return true;
    end if;
  	return false;
END;
$body$
LANGUAGE 'plpgsql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.dodaj_odcinek (
  integer,
  text
)
RETURNS integer AS
$body$
INSERT INTO "projekt"."ODCINEK" (id_sezon, nazwa) VALUES
($1, $2) RETURNING id_sezon
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.dodaj_serial (
  text,
  text,
  integer = '-1'::integer
)
RETURNS integer AS
$body$
INSERT INTO "projekt"."SERIAL" (id_serial, nazwa, opis, rok_produkcji) VALUES
(projekt.next_id('SERIAL', 'id_serial'), $1, $2, $3) RETURNING id_serial
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.dodaj_sezon (
  integer,
  integer = '-1'::integer
)
RETURNS integer AS
$body$
INSERT INTO "projekt"."SEZON" (id_sezon, id_serial, rok_produkcji) VALUES
(projekt.next_id('SEZON', 'id_sezon'), $1, $2) RETURNING id_sezon
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.dodaj_typ_artysty (
  integer,
  text
)
RETURNS integer AS
$body$
INSERT INTO "projekt"."RODZAJ_ARTYSTY" (id_artysta, typ) VALUES
($1, $2) RETURNING id_artysta
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.id_artysty (
  varchar,
  varchar
)
RETURNS integer AS
$body$
SELECT id_artysta 
FROM "projekt"."ARTYSTA"
WHERE upper(imie) = upper($1) and upper(nazwisko) = upper($2)
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.id_filmu (
  varchar
)
RETURNS integer AS
$body$
SELECT id_film 
FROM "projekt"."FILM"
WHERE nazwa = $1
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.id_gry (
  varchar
)
RETURNS integer AS
$body$
SELECT id_gra 
FROM "projekt"."GRA"
WHERE nazwa = $1
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.id_serialu (
  varchar
)
RETURNS integer AS
$body$
SELECT id_serial
FROM "projekt"."SERIAL"
WHERE nazwa = $1
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt."id_użytkownika" (
  varchar
)
RETURNS integer AS
$body$
SELECT id_user 
FROM "projekt"."UZYTKOWNIK"
WHERE email = $1
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.next_id (
  table_name varchar,
  id_what varchar
)
RETURNS integer AS
$body$
DECLARE
  	result integer;
BEGIN
    execute 'SELECT COUNT(*) FROM "projekt"."' || table_name || '"' into result;
	IF(result > 0) THEN
  		execute 'SELECT MAX(' || id_what || ')+1 FROM "projekt"."' || table_name || '"' into result;
    ELSE
    	result = 1;
    END IF;
  	return result;
END;
$body$
LANGUAGE 'plpgsql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.wyszukaj_filmy (
  varchar
)
RETURNS TABLE (
  id_film integer,
  nazwa text
) AS
$body$
        SELECT id_film, nazwa
        FROM "projekt"."FILM" as film        
        WHERE film.nazwa LIKE $1
        ORDER BY nazwa;
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.wyszukaj_gry (
  varchar
)
RETURNS TABLE (
  id_gra integer,
  nazwa varchar
) AS
$body$
        SELECT id_gra, nazwa
        FROM "projekt"."GRA" as gra       
        WHERE gra.nazwa LIKE $1 
        ORDER BY nazwa
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.wyszukaj_info_sezon (
  integer,
  integer
)
RETURNS TABLE (
  nazwa varchar,
  rok_produkcji integer
) AS
$body$
        SELECT nazwa, sezon.rok_produkcji
        FROM "projekt"."SEZON" as sezon JOIN "projekt"."SERIAL" USING(id_serial) 
        WHERE id_serial = $1 and id_sezon = $2
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt."wyszukaj_info_użytkownika" (
  varchar
)
RETURNS TABLE (
  login varchar,
  email varchar,
  data_dolaczenia timestamp
) AS
$body$
        SELECT login, email, data_dolaczenia
        FROM "projekt"."UZYTKOWNIK"
        WHERE email = $1
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.wyszukaj_obserwowanych (
  varchar
)
RETURNS TABLE (
  id_user integer,
  login varchar
) AS
$body$
        SELECT id_user, login
        FROM "projekt"."UZYTKOWNIK" JOIN (
        SELECT id_obserwowany 
        FROM "projekt"."UZYTKOWNIK" JOIN "projekt"."OBSERWOWANY" USING(id_user)
        WHERE email = $1) as p 
        ON p.id_obserwowany = id_user
        UNION
        SELECT id_user, login
        FROM "projekt"."UZYTKOWNIK"
        WHERE email = $1
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.wyszukaj_odcinki (
  integer
)
RETURNS TABLE (
  nazwa varchar
) AS
$body$
        SELECT nazwa 
        FROM "projekt"."ODCINEK" 
        WHERE id_sezon = $1
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt."wyszukaj_rodzaj_artystów" (
  integer
)
RETURNS TABLE (
  typ varchar
) AS
$body$
        SELECT typ
        FROM "projekt"."RODZAJ_ARTYSTY"
        WHERE id_artysta = $1
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.wyszukaj_role (
  integer
)
RETURNS TABLE (
  nazwa varchar,
  rola varchar,
  postac varchar,
  rok_produkcji integer
) AS
$body$
        (SELECT nazwa, rola, postac, rok_produkcji
        FROM "projekt"."ARTYSTA" JOIN "projekt"."ARTYSTA_FILM" USING(id_artysta)
                                 JOIN "projekt"."FILM" as film USING(id_film)
        WHERE id_artysta = $1
        UNION
        SELECT nazwa, rola, postac, rok_produkcji
        FROM "projekt"."ARTYSTA" JOIN "projekt"."ARTYSTA_SERIAL" USING(id_artysta)
                                 JOIN "projekt"."SERIAL" as serial USING(id_serial)
        WHERE id_artysta = $1)
        ORDER BY rok_produkcji
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.wyszukaj_seriale (
  varchar
)
RETURNS TABLE (
  id_serial integer,
  nazwa varchar
) AS
$body$
        SELECT id_serial, nazwa
        FROM "projekt"."SERIAL" as serial 
        WHERE serial.nazwa LIKE $1
        ORDER BY nazwa
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.wyszukaj_sezony (
  integer
)
RETURNS SETOF projekt."SEZON" AS
$body$
        SELECT * 
        FROM "projekt"."SEZON" 
        WHERE id_serial = $1;
$body$
LANGUAGE 'sql'
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt."wyszukaj_użytkowników" (
  varchar,
  varchar
)
RETURNS TABLE (
  id_user integer,
  login varchar
) AS
$body$
        SELECT id_user, login
        FROM "projekt"."UZYTKOWNIK"
        WHERE email != $1 and login LIKE $2
$body$
LANGUAGE 'sql'
