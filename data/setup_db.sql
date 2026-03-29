CREATE DATABASE IF NOT EXISTS sudoku_solver;
USE sudoku_solver;

-- Table pour stocker les grilles
CREATE TABLE IF NOT EXISTS grilles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grille_initiale TEXT NOT NULL,
    cases_vides INT NOT NULL,
    date_import DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table pour stocker les resultats de resolution
CREATE TABLE IF NOT EXISTS resolutions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grille_id INT NOT NULL,
    methode VARCHAR(50) NOT NULL,
    grille_resolue TEXT,
    temps_execution FLOAT NOT NULL,
    iterations INT NOT NULL,
    backtracks INT DEFAULT 0,
    verifications INT NOT NULL,
    memoire_max BIGINT DEFAULT 0,
    nb_snapshots INT DEFAULT 0,
    succes BOOLEAN DEFAULT TRUE,
    date_resolution DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grille_id) REFERENCES grilles(id)
);
