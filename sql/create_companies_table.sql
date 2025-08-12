CREATE TABLE IF NOT EXISTS company (
        company_number TEXT PRIMARY KEY,
        company_name TEXT,
        company_category TEXT,
        company_status TEXT,
        dissolution_date DATE,
        incorporation_date DATE, 
        full_address TEXT,
        care_of TEXT,
        post_box TEXT,
        address_line_1 TEXT,
        address_line_2 TEXT,
        post_town TEXT,
        county TEXT,
        country TEXT,
        post_code TEXT
    );