CREATE TABLE projekt."ARTYSTA" (
  id_artysta INTEGER NOT NULL,
  imie VARCHAR(30) NOT NULL,
  nazwisko VARCHAR(30) NOT NULL,
  data_urodzenia INTEGER,
  data_smierci INTEGER,
  CONSTRAINT "ARTYSTA_pkey" PRIMARY KEY(id_artysta)
) 
-----------------------------------------------------------
CREATE TABLE projekt."ARTYSTA_FILM" (
  id_artysta INTEGER NOT NULL,
  id_film INTEGER NOT NULL,
  rola VARCHAR(30),
  postac VARCHAR(30),
  CONSTRAINT "ARTYSTA_FILM_fk_artysta" FOREIGN KEY (id_artysta)
    REFERENCES projekt."ARTYSTA"(id_artysta)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE,
  CONSTRAINT "ARTYSTA_FILM_fk_film" FOREIGN KEY (id_film)
    REFERENCES projekt."FILM"(id_film)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE
) 
-----------------------------------------------------------
CREATE TABLE projekt."ARTYSTA_SERIAL" (
  id_artysta INTEGER NOT NULL,
  id_serial INTEGER NOT NULL,
  rola VARCHAR(30),
  postac VARCHAR(30),
  CONSTRAINT "ARTYSTA_SERIAL_artysta" FOREIGN KEY (id_artysta)
    REFERENCES projekt."ARTYSTA"(id_artysta)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE,
  CONSTRAINT "ARTYSTA_SERIAL_fk_serial" FOREIGN KEY (id_serial)
    REFERENCES projekt."SERIAL"(id_serial)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE
) 
-----------------------------------------------------------
CREATE TABLE projekt."FILM" (
  id_film INTEGER NOT NULL,
  nazwa VARCHAR(30) NOT NULL,
  opis VARCHAR(300),
  rok_produkcji INTEGER,
  box_office VARCHAR(20),
  studio VARCHAR(30),
  CONSTRAINT "FILM_pkey" PRIMARY KEY(id_film)
)
-----------------------------------------------------------
CREATE TABLE projekt."GRA" (
  id_gra INTEGER NOT NULL,
  nazwa VARCHAR(30) NOT NULL,
  opis VARCHAR(300),
  rok_produkcji INTEGER,
  studio VARCHAR(30),
  sprzedaz VARCHAR(20),
  CONSTRAINT "GRA_pkey" PRIMARY KEY(id_gra)
)
-----------------------------------------------------------
CREATE TABLE projekt."KOMENTARZ" (
  id_komentarz INTEGER NOT NULL,
  id_film_opinia INTEGER,
  id_serial_opinia INTEGER,
  id_gra_opinia INTEGER,
  recenzja VARCHAR(300) NOT NULL,
  CONSTRAINT "KOMENTARZ_pkey" PRIMARY KEY(id_komentarz),
  CONSTRAINT "KOMENTARZ_fk_film" FOREIGN KEY (id_film_opinia)
    REFERENCES projekt."UZYTKOWNIK_FILM"(id_film_opinia)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE,
  CONSTRAINT "KOMENTARZ_fk_gra" FOREIGN KEY (id_gra_opinia)
    REFERENCES projekt."UZYTKOWNIK_GRA"(id_gra_opinia)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE,
  CONSTRAINT "KOMENTARZ_fk_serial" FOREIGN KEY (id_serial_opinia)
    REFERENCES projekt."UZYTKOWNIK_SERIAL"(id_serial_opinia)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE
)
-----------------------------------------------------------
CREATE TABLE projekt."NAGRODA" (
  id_film INTEGER,
  id_serial INTEGER,
  id_gra INTEGER,
  id_artysta INTEGER,
  rok_przyznania INTEGER,
  nazwa VARCHAR(100) NOT NULL,
  CONSTRAINT "NAGRODA_fk_artysta" FOREIGN KEY (id_artysta)
    REFERENCES projekt."ARTYSTA"(id_artysta)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE,
  CONSTRAINT "NAGRODA_fk_film" FOREIGN KEY (id_film)
    REFERENCES projekt."FILM"(id_film)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE,
  CONSTRAINT "NAGRODA_fk_gra" FOREIGN KEY (id_gra)
    REFERENCES projekt."GRA"(id_gra)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE,
  CONSTRAINT "NAGRODA_fk_serial" FOREIGN KEY (id_serial)
    REFERENCES projekt."SERIAL"(id_serial)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE
) 
-----------------------------------------------------------
CREATE TABLE projekt."OBSERWOWANY" (
  id_user INTEGER NOT NULL,
  id_obserwowany INTEGER NOT NULL,
  data_obserwacji TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL,
  CONSTRAINT "OBSERWOWANY_fk" FOREIGN KEY (id_user)
    REFERENCES projekt."UZYTKOWNIK"(id_user)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE
) 
-----------------------------------------------------------
CREATE TABLE projekt."ODCINEK" (
  id_sezon INTEGER NOT NULL,
  nazwa VARCHAR(100) NOT NULL,
  CONSTRAINT "ODCINEK_fk" FOREIGN KEY (id_sezon)
    REFERENCES projekt."SEZON"(id_sezon)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE
) 
-----------------------------------------------------------
CREATE TABLE projekt."RODZAJ_ARTYSTY" (
  id_artysta INTEGER,
  typ VARCHAR(30) NOT NULL,
  CONSTRAINT "RODZAJ_ARTYSTY_fk" FOREIGN KEY (id_artysta)
    REFERENCES projekt."ARTYSTA"(id_artysta)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE
) 
-----------------------------------------------------------
CREATE TABLE projekt."SERIAL" (
  id_serial INTEGER NOT NULL,
  nazwa VARCHAR(30) NOT NULL,
  opis VARCHAR(300),
  rok_produkcji INTEGER,
  CONSTRAINT "SERIAL_pkey" PRIMARY KEY(id_serial)
) 
-----------------------------------------------------------
CREATE TABLE projekt."SEZON" (
  id_sezon INTEGER NOT NULL,
  id_serial INTEGER,
  rok_produkcji INTEGER,
  CONSTRAINT "SEZON_pkey" PRIMARY KEY(id_sezon),
  CONSTRAINT "SEZON_fk" FOREIGN KEY (id_serial)
    REFERENCES projekt."SERIAL"(id_serial)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE
) 
-----------------------------------------------------------
CREATE TABLE projekt."UZYTKOWNIK" (
  id_user INTEGER NOT NULL,
  email VARCHAR(30) NOT NULL,
  data_dolaczenia TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL,
  haslo VARCHAR(50) NOT NULL,
  login VARCHAR(30) NOT NULL,
  CONSTRAINT "UZYTKOWNIK_pkey" PRIMARY KEY(id_user)
) 
-----------------------------------------------------------
CREATE TABLE projekt."UZYTKOWNIK_FILM" (
  id_film_opinia INTEGER NOT NULL,
  id_user INTEGER NOT NULL,
  id_film INTEGER NOT NULL,
  ocena INTEGER,
  data_oceny TIMESTAMP(6) WITHOUT TIME ZONE,
  CONSTRAINT "UZYTKOWNIK_FILM_pkey" PRIMARY KEY(id_film_opinia),
  CONSTRAINT "UZYTKOWNIK_FILM_film" FOREIGN KEY (id_film)
    REFERENCES projekt."FILM"(id_film)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE,
  CONSTRAINT "UZYTKOWNIK_FILM_fk_user" FOREIGN KEY (id_user)
    REFERENCES projekt."UZYTKOWNIK"(id_user)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE
) 
-----------------------------------------------------------
CREATE TABLE projekt."UZYTKOWNIK_GRA" (
  id_gra_opinia INTEGER NOT NULL,
  id_user INTEGER NOT NULL,
  id_gra INTEGER NOT NULL,
  ocena INTEGER,
  data_oceny TIMESTAMP(6) WITHOUT TIME ZONE,
  CONSTRAINT "UZYTKOWNIK_GRA_pkey" PRIMARY KEY(id_gra_opinia),
  CONSTRAINT "UZYTKOWNIK_GRA_fk_gra" FOREIGN KEY (id_gra)
    REFERENCES projekt."GRA"(id_gra)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE,
  CONSTRAINT "UZYTKOWNIK_GRA_fk_user" FOREIGN KEY (id_user)
    REFERENCES projekt."UZYTKOWNIK"(id_user)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE
) 
-----------------------------------------------------------
CREATE TABLE projekt."UZYTKOWNIK_SERIAL" (
  id_serial_opinia INTEGER NOT NULL,
  id_user INTEGER NOT NULL,
  id_serial INTEGER NOT NULL,
  ocena INTEGER,
  data_oceny TIMESTAMP(6) WITHOUT TIME ZONE,
  CONSTRAINT "UZYTKOWNIK_SERIAL_pkey" PRIMARY KEY(id_serial_opinia),
  CONSTRAINT "UZYTKOWNIK_SERIAL_fk_serial" FOREIGN KEY (id_serial)
    REFERENCES projekt."SERIAL"(id_serial)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE,
  CONSTRAINT "UZYTKOWNIK_SERIAL_fk_user" FOREIGN KEY (id_user)
    REFERENCES projekt."UZYTKOWNIK"(id_user)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    NOT DEFERRABLE
) 	
	
	
	
	
	