CREATE TABLE IF NOT EXISTS WatchedHistory (
        whKey           INTEGER NOT NULL UNIQUE AUTO_INCREMENT,
        whDate          DATE NOT NULL,
        whTitle         VARCHAR(150) NOT NULL,
        whYear         	INTEGER NOT NULL,
        whRottenScore   INTEGER NOT NULL,
        whMyScore       INTEGER NOT NULL,
        whNotes         VARCHAR(500),
        PRIMARY KEY(whKey)
);
