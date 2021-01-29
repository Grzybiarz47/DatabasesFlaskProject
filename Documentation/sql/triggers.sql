CREATE OR REPLACE FUNCTION projekt.valid_email ()
RETURNS trigger AS
$body$
BEGIN
  if((SELECT COUNT(*) FROM "projekt"."UZYTKOWNIK" WHERE email=New.email or login=New.login) > 0) then
  	raise info 'Email jest już w bazie';
    return NULL;
  else
  	raise info 'Rejestruję uzytkownika';
    return new;
  end if;
END;
$body$
LANGUAGE 'plpgsql'

CREATE TRIGGER rejestracja_wyzwalacz
  BEFORE INSERT 
  ON projekt."UZYTKOWNIK"
  
FOR EACH ROW 
  EXECUTE PROCEDURE projekt.valid_email();
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION projekt.valid_comment ()
RETURNS trigger AS
$body$
BEGIN
	if(New.recenzja <> '') then
		return New;
    else
    	return NULL;
	end if;
END;
$body$
LANGUAGE 'plpgsql'

CREATE TRIGGER nowy_komentarz_wyzwalacz
  BEFORE INSERT 
  ON projekt."KOMENTARZ"
  
FOR EACH ROW 
  EXECUTE PROCEDURE projekt.valid_comment();
