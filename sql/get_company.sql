SELECT
company.company_number,
company.company_name,
company.full_address,
psc.full_name,
psc.full_address

FROM company
JOIN psc ON company.company_number = psc.company_number
WHERE company.company_name == :entity_name;
