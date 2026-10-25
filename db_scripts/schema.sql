USE ecocompute;

CREATE TABLE clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    contact_email VARCHAR(150) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE server_zones (
    zone_id INT AUTO_INCREMENT PRIMARY KEY,
    zone_name VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(100) NOT NULL,
    cooling_type VARCHAR(50) NOT NULL
);

CREATE TABLE server_racks (
    rack_id INT AUTO_INCREMENT PRIMARY KEY,
    rack_name VARCHAR(100) NOT NULL UNIQUE,
    zone_id INT NOT NULL,
    client_id INT NOT NULL,
    power_draw_kw DECIMAL(8,2) NOT NULL,
    installed_on DATE,
    CONSTRAINT chk_power_draw CHECK (power_draw_kw >= 0),
    CONSTRAINT fk_rack_zone
        FOREIGN KEY (zone_id) REFERENCES server_zones(zone_id),
    CONSTRAINT fk_rack_client
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

CREATE TABLE maintenance_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    rack_id INT NOT NULL,
    maintenance_date DATETIME NOT NULL,
    issue_type VARCHAR(100) NOT NULL,
    description TEXT,
    status ENUM('Open', 'In Progress', 'Resolved')
        NOT NULL DEFAULT 'Open',
    technician VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_log_rack
        FOREIGN KEY (rack_id) REFERENCES server_racks(rack_id)
);

CREATE INDEX idx_racks_zone
    ON server_racks(zone_id);

CREATE INDEX idx_logs_rack_date
    ON maintenance_logs(rack_id, maintenance_date);

CREATE INDEX idx_logs_status
    ON maintenance_logs(status);
