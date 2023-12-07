CREATE TABLE usuarios(
    correo varchar,
    password varchar,
    token varchar,
    timestamp varchar
);

INSERT INTO usuarios (correo, password, token, timestamp) VALUES ('amairani@correo.com', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '1234', DateTime('now')) ;
