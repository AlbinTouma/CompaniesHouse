# Know Your Business Owners API

KYBO is a Restful API for querying persons of significant control and companies in the UK company register, Companies House.

## Ingestion

There are currently no endpoints to connect directly to UKCH's own API or to ingest PSC and Company data from a file. 
Instead, download the files from UKCH and place them in the root of the directory. Make sure the files are named psc.txt and companies.csv.
Use the bash script to run the ingestion process. 
The ingestor creates a sqlite database inside the database folder.

## API endpoints

KYBO has two endpoints: companies and psc. 

- The companies endpoint returns either company data or company data with a list of persons with significant control over the company.
- The psc endpoint lets returns either information about the person of significant control or information about the person of significant control and firmographic data of the company where the person has control.

## Future ideas

Ideally you would be able to search for a PSC and return a list of all of the companies that they own. 
Today querying for all companies where a PSC has significant control or ownership is unfortunately not possible. This is because the person_id provided by UKCH is not a unique identifier of the person of significant control. 
A future release might include creating a unique id for PSCs and an endpoint to query all of the companies where they have significant ownership or control.

Ownership data is often visualised with a grap to show the connections between companies and officers and a popular format is BODs statements. 
A possible feature in the future is the ability to create BODs statements from company and PSC data for visualising relationships.

