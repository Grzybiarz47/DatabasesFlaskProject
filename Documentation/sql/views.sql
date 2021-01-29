CREATE VIEW projekt."statystyki_najwyższe_oceny" (
    nazwa,
    sr_ocena)
AS
WITH cte(nazwa, sr_ocena) AS (
SELECT "FILM".nazwa, avg("UZYTKOWNIK_FILM".ocena) AS sr_ocena
FROM projekt."FILM" JOIN projekt."UZYTKOWNIK_FILM" USING (id_film)
GROUP BY "FILM".nazwa
HAVING avg("UZYTKOWNIK_FILM".ocena) > 8.0
UNION
SELECT "SERIAL".nazwa, avg("UZYTKOWNIK_SERIAL".ocena) AS sr_ocena
FROM projekt."SERIAL" JOIN projekt."UZYTKOWNIK_SERIAL" USING (id_serial)
GROUP BY "SERIAL".nazwa
HAVING avg("UZYTKOWNIK_SERIAL".ocena) > 8.0
UNION
SELECT "GRA".nazwa, avg("UZYTKOWNIK_GRA".ocena) AS sr_ocena
FROM projekt."GRA" JOIN projekt."UZYTKOWNIK_GRA" USING (id_gra)
GROUP BY "GRA".nazwa
HAVING avg("UZYTKOWNIK_GRA".ocena) > 8.0
)
    SELECT cte.nazwa,
    cte.sr_ocena::numeric(7,4) AS sr_ocena
    FROM cte
    ORDER BY cte.sr_ocena DESC
    LIMIT 15;
-----------------------------------------------------------
CREATE OR REPLACE VIEW projekt."statystyki_ogólne" (
    l_art,
    l_ser,
    l_fil,
    l_gra,
    l_kom,
    l_ocen_film,
    sr_ocen_film,
    l_ocen_serial,
    sr_ocen_serial,
    l_ocen_gra,
    sr_ocen_gra)
AS
SELECT (
    SELECT count(*) AS l_art
    FROM projekt."ARTYSTA"
    ) AS l_art,
    (
    SELECT count(*) AS l_ser
    FROM projekt."SERIAL"
    ) AS l_ser,
    (
    SELECT count(*) AS l_fil
    FROM projekt."FILM"
    ) AS l_fil,
    (
    SELECT count(*) AS l_gra
    FROM projekt."GRA"
    ) AS l_gra,
    (
    SELECT count(*) AS l_kom
    FROM projekt."KOMENTARZ"
    ) AS l_kom,
    (
    SELECT count("UZYTKOWNIK_FILM".ocena) AS l_ocen_film
    FROM projekt."UZYTKOWNIK_FILM"
    ) AS l_ocen_film,
    (
    SELECT avg("UZYTKOWNIK_FILM".ocena)::numeric(7,4) AS sr_ocen_film
    FROM projekt."UZYTKOWNIK_FILM"
    ) AS sr_ocen_film,
    (
    SELECT count("UZYTKOWNIK_SERIAL".ocena) AS l_ocen_serial
    FROM projekt."UZYTKOWNIK_SERIAL"
    ) AS l_ocen_serial,
    (
    SELECT avg("UZYTKOWNIK_SERIAL".ocena)::numeric(7,4) AS sr_ocen_serial
    FROM projekt."UZYTKOWNIK_SERIAL"
    ) AS sr_ocen_serial,
    (
    SELECT count("UZYTKOWNIK_GRA".ocena) AS l_ocen_gra
    FROM projekt."UZYTKOWNIK_GRA"
    ) AS l_ocen_gra,
    (
    SELECT avg("UZYTKOWNIK_GRA".ocena)::numeric(7,4) AS sr_ocen_gra
    FROM projekt."UZYTKOWNIK_GRA"
    ) AS sr_ocen_gra;
-----------------------------------------------------------
CREATE OR REPLACE VIEW projekt."statystyki_typy_artystów" (
    typ,
    l_typ)
AS
SELECT "RODZAJ_ARTYSTY".typ, count(*) AS l_typ
FROM projekt."RODZAJ_ARTYSTY"
GROUP BY "RODZAJ_ARTYSTY".typ
ORDER BY "RODZAJ_ARTYSTY".typ;
	
	