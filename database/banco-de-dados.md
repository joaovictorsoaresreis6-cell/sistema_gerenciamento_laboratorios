\# Banco de Dados — Sistema de Gerenciamento de Laboratórios



\## 1. Tecnologia utilizada



O sistema utiliza PostgreSQL como sistema gerenciador de banco de dados.



A aplicação utiliza Python com FastAPI no backend e SQLAlchemy como ORM para realizar a comunicação entre a API e o banco de dados.



Fluxo de acesso aos dados:



PostgreSQL → Tabelas → Relacionamentos → SQLAlchemy/ORM → API FastAPI → CRUD



\---



\## 2. Estrutura do banco



O banco de dados utilizado pelo sistema é:



`sistema\_laboratorios`



As tabelas implementadas são:



\- usuario

\- laboratorio

\- computador

\- professor

\- aula

\- manutencao

\- reserva

\- notificacao



Essas tabelas correspondem às entidades definidas no modelo de classes do sistema.



\---



\## 3. Tabela Usuario



Representa os usuários que realizam operações no sistema.



Principais campos:



| Campo | Tipo | Restrição |

|---|---|---|

| idUsuario | INTEGER | PK, NOT NULL |

| nome | VARCHAR(100) | NOT NULL |

| email | VARCHAR(150) | NOT NULL, UNIQUE |

| tipo | VARCHAR(50) | NOT NULL |

| senha | VARCHAR(255) | NOT NULL |



\---



\## 4. Tabela Laboratorio



Armazena os laboratórios disponíveis na instituição.



| Campo | Tipo | Restrição |

|---|---|---|

| idLaboratorio | INTEGER | PK, NOT NULL |

| nome | VARCHAR(100) | NOT NULL, UNIQUE |

| localizacao | VARCHAR(150) | NOT NULL |

| capacidade | INTEGER | NOT NULL |

| status | VARCHAR(30) | NOT NULL |



\---



\## 5. Tabela Computador



Representa os computadores pertencentes aos laboratórios.



| Campo | Tipo | Restrição |

|---|---|---|

| idComputador | INTEGER | PK, NOT NULL |

| patrimonio | VARCHAR(50) | NOT NULL, UNIQUE |

| especificacao | VARCHAR(255) | NULL |

| status | VARCHAR(30) | NOT NULL |

| idLaboratorio | INTEGER | FK, NOT NULL |



Relacionamento:



`computador.idLaboratorio → laboratorio.idLaboratorio`



\---



\## 6. Tabela Professor



Armazena os professores cadastrados.



| Campo | Tipo | Restrição |

|---|---|---|

| idProfessor | INTEGER | PK, NOT NULL |

| nome | VARCHAR(100) | NOT NULL |

| email | VARCHAR(150) | NOT NULL, UNIQUE |

| matricula | VARCHAR(50) | NOT NULL, UNIQUE |



\---



\## 7. Tabela Aula



Representa as aulas agendadas nos laboratórios.



| Campo | Tipo | Restrição |

|---|---|---|

| idAula | INTEGER | PK, NOT NULL |

| disciplina | VARCHAR(100) | NOT NULL |

| data | DATE | NOT NULL |

| horaInicio | TIME | NOT NULL |

| horaFim | TIME | NOT NULL |

| idProfessor | INTEGER | FK, NOT NULL |

| idLaboratorio | INTEGER | FK, NOT NULL |



Relacionamentos:



`aula.idProfessor → professor.idProfessor`



`aula.idLaboratorio → laboratorio.idLaboratorio`



\---



\## 8. Tabela Manutencao



Armazena os períodos de manutenção dos laboratórios.



| Campo | Tipo | Restrição |

|---|---|---|

| idManutencao | INTEGER | PK, NOT NULL |

| dataInicio | DATE | NOT NULL |

| dataFim | DATE | NOT NULL |

| motivo | VARCHAR(255) | NOT NULL |

| status | VARCHAR(30) | NOT NULL |

| idLaboratorio | INTEGER | FK, NOT NULL |



Relacionamento:



`manutencao.idLaboratorio → laboratorio.idLaboratorio`



\---



\## 9. Tabela Reserva



Armazena as reservas realizadas pelos usuários.



| Campo | Tipo | Restrição |

|---|---|---|

| idReserva | INTEGER | PK, NOT NULL |

| data | DATE | NOT NULL |

| horaInicio | TIME | NOT NULL |

| horaFim | TIME | NOT NULL |

| status | VARCHAR(30) | NOT NULL |

| idUsuario | INTEGER | FK, NOT NULL |

| idLaboratorio | INTEGER | FK, NOT NULL |



Relacionamentos:



`reserva.idUsuario → usuario.idUsuario`



`reserva.idLaboratorio → laboratorio.idLaboratorio`



\---



\## 10. Tabela Notificacao



Armazena notificações relacionadas às reservas.



| Campo | Tipo | Restrição |

|---|---|---|

| idNotificacao | INTEGER | PK, NOT NULL |

| mensagem | VARCHAR(255) | NOT NULL |

| dataHora | TIMESTAMP | NOT NULL |

| tipo | VARCHAR(50) | NOT NULL |

| idReserva | INTEGER | FK, NOT NULL |

| idUsuario | INTEGER | FK, NOT NULL |



Relacionamentos:



`notificacao.idReserva → reserva.idReserva`



`notificacao.idUsuario → usuario.idUsuario`



\---



\## 11. Relacionamentos



Os principais relacionamentos implementados são:



\- Um Professor pode estar relacionado a várias Aulas.

\- Um Laboratório pode possuir várias Aulas.

\- Um Laboratório pode possuir vários Computadores.

\- Um Laboratório pode possuir várias Manutenções.

\- Um Laboratório pode possuir várias Reservas.

\- Um Usuário pode realizar várias Reservas.

\- Uma Reserva pode gerar várias Notificações.

\- Um Usuário pode receber várias Notificações.



\---



\## 12. Integridade do banco



Foram implementadas as seguintes restrições:



\### Chaves primárias



Cada tabela possui uma chave primária para identificar seus registros.



\### Chaves estrangeiras



As chaves estrangeiras garantem que os registros relacionados existam nas tabelas correspondentes.



\### NOT NULL



Os campos obrigatórios não permitem valores nulos.



\### UNIQUE



Foram utilizadas restrições de unicidade para evitar duplicidade em:



\- email de usuário;

\- nome de laboratório;

\- patrimônio de computador;

\- email de professor;

\- matrícula de professor.



\### Integridade referencial



O PostgreSQL impede a inserção de registros que apontem para entidades inexistentes.



Durante os testes, uma tentativa de criar uma reserva com `idUsuario = 9999` foi rejeitada pelo PostgreSQL por violação da chave estrangeira.



\---



\## 13. Seed



O arquivo `seed.sql` contém dados básicos para desenvolvimento e demonstração.



Localização:



`database/seed.sql`



Os dados incluem:



\- usuário de demonstração;

\- professor de demonstração;

\- dois laboratórios;

\- computadores;

\- uma aula;

\- um período de manutenção.



As reservas não são inseridas automaticamente pelo seed, pois podem ser criadas durante a demonstração do caso de uso de realização de reserva.



\---



\## 14. Comunicação com a API



A API FastAPI utiliza o SQLAlchemy para acessar o PostgreSQL.



Fluxo:



```text

Usuário

&#x20;  ↓

API FastAPI

&#x20;  ↓

SQLAlchemy / ORM

&#x20;  ↓

PostgreSQL

&#x20;  ↓

Tabelas

