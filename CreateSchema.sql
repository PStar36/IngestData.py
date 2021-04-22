
-- Cleanup existing tables and data
DROP TABLE IF EXISTS Games, Countries, Cities, GamesIn, 
  Teams, Athletes, TeamAthletes, Events, Results, TEMPEVENTS, Tempgames,TCities;

-- Create all tables, incl constraints
CREATE TABLE TEMPEVENTS(
  TEKey SERIAL PRIMARY KEY,
  TEventName VARCHAR(128) NOT NULL,
  TSportName VARCHAR(32) NOT NULL,
  TAKey INT,
  TName VARCHAR(128) NOT NULL,
  TGender CHAR,
  TDoB DATE,
  THeight INT,
  TWeight INT,
  TTName VARCHAR(128),
  TTNoc CHAR(3),
  TTYear INT,
  );
create TABLE Tempgames(
  TYear INT,
  TName VARCHAR(32)  ,
  TStartDate Date ,
  TEndDate Date
);
CREATE TABLE Games(
  Year INT PRIMARY KEY,
  Name VARCHAR(32) NOT NULL,
  StartDate Date NOT NULL,
  EndDate Date NOT NULL
);

CREATE TABLE Countries(
  Noc CHAR(3) PRIMARY KEY,
  Name VARCHAR(128) UNIQUE NOT NULL,
  Population BIGINT,
  Gdp FLOAT
);

CREATE TABLE Cities(
  CKey SERIAL PRIMARY KEY,
  Name VARCHAR(128) UNIQUE NOT NULL,
  Noc CHAR(3) REFERENCES Countries NOT NULL
);

CREATE TABLE TCities(
    TCKey SERIAL PRIMARY KEY,
    TName VARCHAR(128)  NOT NULL,
    TNoc CHAR(3) REFERENCES Countries NOT NULL,
    YEAR INT
);

CREATE TABLE GamesIn(
  Year INT REFERENCES Games,
  CKey INT REFERENCES Cities,
  PRIMARY KEY(Year, CKey)
);

CREATE TABLE Teams(
  TKey SERIAL PRIMARY KEY,
  Name VARCHAR(128) NOT NULL,
  Noc CHAR(3) REFERENCES Countries NOT NULL,
  Year INT REFERENCES Games NOT NULL,
  UNIQUE(Name,Year)
);

CREATE TABLE Athletes(
  AKey INT PRIMARY KEY,
  Name VARCHAR(128) NOT NULL,
  Gender CHAR,
  DoB DATE, 
  Height INT, 
  Weight INT 
);

CREATE TABLE TeamAthletes(
  TKey INT REFERENCES Teams,
  AKey INT REFERENCES Athletes,
  PRIMARY KEY(AKey, TKey)
);

CREATE TABLE Events(
  EKey SERIAL PRIMARY KEY,
  EventName VARCHAR(128) UNIQUE NOT NULL,
  SportName VARCHAR(32) NOT NULL
);


CREATE TABLE Results(
  Year INT REFERENCES Games,
  EKey INT REFERENCES Events,
  AKey INT REFERENCES Athletes,
  Medal CHAR(1) CHECK(Medal IN('G','S','B')),
  PRIMARY KEY(Year, EKey, AKey)
);
