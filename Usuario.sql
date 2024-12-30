DROP DATABASE IF EXISTS Usuario;
create database Usuario;
use Usuario;

create table usuarios (
    codigo varchar(25) PRIMARY KEY,
    area varchar(25),                
    puesto varchar(25),              
    nombre varchar(50),              
    extencion int   
);
 
INSERT INTO usuarios (codigo, area, puesto, nombre,extencion)
VALUES ('N/A', 'Administrativa', 'Recepcion', 'Jessica Paola Tellez Molina', 155);

SELECT * FROM usuarios;