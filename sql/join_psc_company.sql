SELECT
company.company_number,
company.company_name,
psc.full_name,
psc.registration_number,
psc.legal_form,
psc.full_address
FROM company
JOIN psc ON company.company_number = psc.company_number
WHERE company.company_name == :company_name;
