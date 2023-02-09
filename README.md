
nombre y atributos de la tabla


CREATE TABLE IF NOT EXISTS docente(
id SERIAL PRIMARY KEY NOT NULL,
nombre VARCHAR(255) NOT NULL,
apellido VARCHAR(255) NOT NULL,
catedra VARCHAR(255) NOT NULL,
facultad VARCHAR(255) NOT NULL,
paralelo VARCHAR(255) NOT NULL,
jornada VARCHAR(255) NOT NULL
);

select * from docente