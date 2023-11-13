-- creamos la base de datos

--create database constructora;

-- 1.- copiamos las tablas

--Tabla empresa
create table empresa (
    id_empresa integer not null,
    nombre varchar not null,
    direccion varchar not null,
    telefono bigint not null,
    correo varchar not null,
    CONSTRAINT empresa_pkey PRIMARY KEY (id_empresa)
);

--Tabla solicitud de proyecto
create table solicitud_proyecto (
    id_solicitud integer not null,
    id_empresa integer not null,
    fecha date not null,
    monto_presupuesto float not null,
    monto_anticipo float not null,
    folio_solicitud varchar not null, --podemos generarlo automaticamente
    estado varchar not null,
    CONSTRAINT solicitud_proyecto_pkey PRIMARY KEY (id_solicitud),
    CONSTRAINT solicitud_empresa_fkey foreign key (id_empresa) references empresa (id_empresa)
);

-- Tabla Proyectos aceptados
create table proyecto (
    id_proyecto integer not null,
    id_empresa integer not null,
    id_solicitud integer not null,
    fecha_inicio date not null,
    fecha_fin date not null,
    monto float not null,
    prioridad varchar not null,
    porcentaje_avance numeric not null,
    estado_proyecto varchar not null,
    CONSTRAINT proyecto_pkey PRIMARY KEY (id_proyecto),
    CONSTRAINT proyecto_empresa_fkey foreign key (id_empresa) references empresa (id_empresa),
    CONSTRAINT proyecto_solicitud_fkey foreign key (id_solicitud) references solicitud_proyecto (id_solicitud)
);

-- Tabla servicio
create table servicio (
    id_servicio integer not null,
    servicio varchar not null,
    descripcion varchar not null,
    CONSTRAINT servicio_pkey PRIMARY KEY (id_servicio)
);

-- Tabla para el detalle de la solicitud
create table detalle_solicitud (
    id_detalle_solicitud integer not null,
    id_solicitud integer not null,
    descripcion varchar not null,
    costo float not null,
    CONSTRAINT detalle_solicitud_pkey PRIMARY KEY (id_detalle_solicitud, id_solicitud),
    CONSTRAINT detalle_solicitud_soli_fkey foreign key (id_solicitud) references solicitud_proyecto (id_solicitud)
);

-- Crear una tabla intermedia para la relación muchos a muchos entre servicio y detalle_solicitud
create table servicio_detalle_solicitud (
    id_servicio_detalle_solicitud integer not null,
    id_servicio integer not null,
    id_detalle_solicitud integer not null,
    id_solicitud integer not null,
    CONSTRAINT servicio_detalle_solicitud_pkey PRIMARY KEY (id_servicio_detalle_solicitud),
    CONSTRAINT servicio_detalle_solicitud_servicio_fkey foreign key (id_servicio) references servicio (id_servicio),
    CONSTRAINT servicio_detalle_solicitud_detalle_fkey foreign key (id_detalle_solicitud, id_solicitud) references detalle_solicitud (id_detalle_solicitud, id_solicitud)
);

-- Tabla supervisor
create table supervisor (
    id_supervisor integer not null,
    nombre varchar not null,
    cargo varchar not null,
    telefono bigint not null,
    correo varchar not null,
    CONSTRAINT supervisor_pkey PRIMARY KEY (id_supervisor)
);

--Tabla proyecto supervisor
create table proyecto_supervisor (
    id_proyecto_supervisor integer not null,
    id_proyecto integer not null,
    id_supervisor integer not null,
    CONSTRAINT proyecto_supervisor_pkey PRIMARY KEY (id_proyecto_supervisor),
    CONSTRAINT proyecto_supervisor_proyecto_fkey foreign key (id_proyecto) references proyecto (id_proyecto),
    CONSTRAINT proyecto_supervisor_sup_fkey foreign key (id_supervisor) references supervisor (id_supervisor)
);

-- Tabla colaboradores
create table colaborador (
    id_colaborador integer not null,
    id_supervisor integer not null,
    nombre varchar not null,
    cargo varchar not null,
    telefono bigint not null,
    correo varchar not null,
    CONSTRAINT colaborador_pkey PRIMARY KEY (id_colaborador, id_supervisor),
    CONSTRAINT supervisor_fkey foreign key (id_supervisor) references supervisor (id_supervisor)
);


-- 2.- creamos secuencias para los id ctrl C + ctrl V

--Secuencias
create sequence empresa_id_empresa;
create sequence solicitud_id_solicitud;
create sequence detalle_solicitud_id_detalle_solicitud;
create sequence servicio_id_servicio;
create sequence detalle_solicitud_servicio_id_detalle_solicitud_servicio;
create sequence proyecto_id_proyecto;
create sequence proyecto_supervisor_id_proyecto_supervisor;
create sequence supervisor_id_supervisor;
create sequence colaborador_id_colaborador;


-------------------------- 3.- Creacion de usuarios y permisos ------------------------------
CREATE user administrador_ct with password 'admin';
CREATE user cliente with password 'cliente';

GRANT USAGE ON SCHEMA public TO administrador_ct;
GRANT USAGE ON SCHEMA public TO cliente;

--privilegios de usuario administrador
GRANT ALL ON table empresa to group administrador_ct;
GRANT ALL On table solicitud_proyecto to group administrador_ct;
GRANT ALL On table detalle_solicitud to group administrador_ct;
GRANT ALL ON table proyecto to group administrador_ct;
GRANT ALL On table servicio to group administrador_ct;
GRANT ALL On table servicio_detalle_solicitud to group administrador_ct;
GRANT ALL On table supervisor to group administrador_ct;
GRANT ALL On table proyecto_supervisor to group administrador_ct;
GRANT ALL On table colaborador to group administrador_ct;

--privilegios de cliente
GRANT ALL ON table empresa to group cliente;
GRANT insert,select,update On table solicitud_proyecto to group cliente;
GRANT insert,select,update On table detalle_solicitud to group cliente;
GRANT insert,select,update ON table proyecto to group cliente;
GRANT ALL On table servicio to group cliente;
GRANT ALL On table servicio_detalle_solicitud to group cliente;
GRANT ALL On table supervisor to group cliente;
GRANT ALL On table proyecto_supervisor to group cliente;
GRANT ALL On table colaborador to group cliente;

--PERMISOS de las secuencias usuario administrador
GRANT ALL on sequence empresa_id_empresa to administrador_ct;
GRANT ALL on sequence solicitud_id_solicitud to administrador_ct;
GRANT ALL on sequence detalle_solicitud_id_detalle_solicitud to administrador_ct;
GRANT ALL on sequence servicio_id_servicio to administrador_ct;
GRANT ALL on sequence detalle_solicitud_servicio_id_detalle_solicitud_servicio to administrador_ct;
GRANT ALL on sequence proyecto_id_proyecto to administrador_ct;
GRANT ALL on sequence proyecto_supervisor_id_proyecto_supervisor to administrador_ct;
GRANT ALL on sequence supervisor_id_supervisor to administrador_ct;
GRANT ALL on sequence colaborador_id_colaborador to administrador_ct;

--PERMISOS de las secuencias usuario cliente
GRANT ALL on sequence empresa_id_empresa to cliente;
GRANT ALL on sequence solicitud_id_solicitud to cliente;
GRANT ALL on sequence detalle_solicitud_id_detalle_solicitud to cliente;
GRANT ALL on sequence servicio_id_servicio to cliente;
GRANT ALL on sequence detalle_solicitud_servicio_id_detalle_solicitud_servicio to cliente;
GRANT ALL on sequence proyecto_id_proyecto to cliente;
GRANT ALL on sequence proyecto_supervisor_id_proyecto_supervisor to cliente;
GRANT ALL on sequence supervisor_id_supervisor to cliente;
GRANT ALL on sequence colaborador_id_colaborador to cliente;


-- 4.- modificamos las tablas para agregar las secuencias ctrl C + ctrl V

ALTER TABLE empresa
ALTER COLUMN id_empresa
SET DEFAULT NEXTVAL('empresa_id_empresa');

ALTER TABLE solicitud_proyecto
ALTER COLUMN id_solicitud
SET DEFAULT NEXTVAL('solicitud_id_solicitud');

ALTER TABLE proyecto
ALTER COLUMN id_proyecto
SET DEFAULT NEXTVAL('proyecto_id_proyecto');

ALTER TABLE servicio
ALTER COLUMN id_servicio
SET DEFAULT NEXTVAL('servicio_id_servicio');

ALTER TABLE detalle_solicitud
ALTER COLUMN id_detalle_solicitud
SET DEFAULT NEXTVAL('detalle_solicitud_id_detalle_solicitud');

ALTER TABLE servicio_detalle_solicitud
ALTER COLUMN id_servicio_detalle_solicitud
SET DEFAULT NEXTVAL('detalle_solicitud_servicio_id_detalle_solicitud_servicio');

ALTER TABLE supervisor
ALTER COLUMN id_supervisor
SET DEFAULT NEXTVAL('supervisor_id_supervisor');

ALTER TABLE proyecto_supervisor
ALTER COLUMN id_proyecto_supervisor
SET DEFAULT NEXTVAL('proyecto_supervisor_id_proyecto_supervisor');

ALTER TABLE colaborador
ALTER COLUMN id_colaborador
SET DEFAULT NEXTVAL('colaborador_id_colaborador');


-- creamos tablas para el login:
CREATE SEQUENCE empleado_id_empleado;
CREATE SEQUENCE cliente_id_cliente;

CREATE TABLE empleado (
    id_empleado INT DEFAULT NEXTVAL('empleado_id_empleado') PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE cliente (
    id_cliente INT DEFAULT NEXTVAL('cliente_id_cliente') PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
