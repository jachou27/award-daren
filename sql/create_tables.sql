CREATE TABLE IF NOT EXISTS hotels (
    hotel_id VARCHAR(50) PRIMARY KEY,
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    category SMALLINT,
    address TEXT,
    city TEXT,
    country TEXT
);

CREATE TABLE IF NOT EXISTS room_types(
    room_type_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hotel_id VARCHAR(50) NOT NULL,
    source_room_type_id VARCHAR(100),
    name TEXT NOT NULL,
    award_type  VARCHAR(50),

    CONSTRAINT fk_room_types_hotel
        FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id),

    CONSTRAINT uq_room_types_source
        UNIQUE (hotel_id, source_room_type_id)

);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    pipeline_run_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL DEFAULT 'running',
    records_extracted INTEGER NOT NULL DEFAULT 0,
    records_loaded INTEGER NOT NULL DEFAULT 0,
    error_message TEXT,

    CONSTRAINT chk_pipeline_status
        CHECK (status IN ('running', 'completed', 'failed')),

    CONSTRAINT chk_records_extracted_nonnegative
        CHECK (records_extracted >= 0),

    CONSTRAINT chk_records_loaded_nonnegative
        CHECK (records_loaded >= 0)

);

CREATE TABLE IF NOT EXISTS daily_availability (
    availability_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    room_type_id BIGINT NOT NULL,
    stay_date DATE NOT NULL,
    award_available BOOLEAN NOT NULL,
    points_price INTEGER,
    cash_price NUMERIC(10,2),
    currency CHAR(3),
    observed_at TIMESTAMPTZ NOT NULL,
    pipeline_run_id BIGINT NOT NULL,

    CONSTRAINT fk_daily_availability_room_type
        FOREIGN KEY (room_type_id) REFERENCES room_types(room_type_id),

    CONSTRAINT fk_daily_availability_pipeline_run 
        FOREIGN KEY (pipeline_run_id) REFERENCES pipeline_runs(pipeline_run_id),

    CONSTRAINT uq_daily_availability_observation
        UNIQUE (room_type_id, stay_date, pipeline_run_id),

    CONSTRAINT chk_points_price_nonnegative
        CHECK (points_price >= 0),

    CONSTRAINT chk_cash_price_nonnegative
        CHECK (cash_price >= 0)
);



