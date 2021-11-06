CREATE TABLE "MediaDimension" (
	"mediaKey"	INTEGER NOT NULL UNIQUE,
	"mediaTitle"	TEXT NOT NULL,
	"mediaYear"	INTEGER NOT NULL,
	"mediaType"	TEXT NOT NULL,
	"mediaHash"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("mediaKey" AUTOINCREMENT)
);

CREATE TABLE "ServiceDimension" (
	"serviceKey"	INTEGER NOT NULL UNIQUE,
	"serviceName"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("serviceKey" AUTOINCREMENT)
);

CREATE TABLE "MediaServiceFact" (
    "MSkey"         INTEGER NOT NULL UNIQUE,
	"MSmediaKey"	INTEGER NOT NULL,
	"MSserviceKey"	INTEGER NOT NULL,
	"MSTimeStamp"	INTEGER,
	PRIMARY KEY("MSkey" AUTOINCREMENT)
	FOREIGN KEY("MSserviceKey") REFERENCES "ServiceDimension"("serviceKey"),
	FOREIGN KEY("MSmediaKey") REFERENCES "MediaDimension"("mediaKey")
);

INSERT INTO ServiceDimension (serviceName)
	VALUES ("HBO Max");
	
INSERT INTO ServiceDimension (serviceName)
	VALUES ("Netflix");
	
INSERT INTO ServiceDimension (serviceName)
	VALUES ("Disney+");
	
INSERT INTO ServiceDimension (serviceName)
	VALUES ("Amazon Prime Video");
	
INSERT INTO ServiceDimension (serviceName)
	VALUES ("Hulu");
	
INSERT INTO ServiceDimension (serviceName)
	VALUES ("Peacock");