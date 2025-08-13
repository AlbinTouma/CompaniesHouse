INSERT OR IGNORE INTO company (
    company_number,
    company_name,
    company_category,
    company_status,
    dissolution_date,
    incorporation_date, 
    full_address,
    care_of, 
    post_box,
    address_line_1,
    address_line_2,
    post_town,
    county,
    country,
    post_code
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
