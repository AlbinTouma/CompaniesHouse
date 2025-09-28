---This script recursively queries company and psc table to find the relationship between pscs and a company


---Store a company's PSCs in a temporary table
CREATE TEMP TABLE PscTemp AS
SELECT * FROM psc WHERE company_number = :company_number;


---For each Psc check if they belong to another company.
CREATE TEMP TABLE corp AS
SELECT * FROM PscTemp WHERE kind Like 'corporate%';

SELECT * FROM corp;