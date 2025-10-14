import json
import uuid
from datetime import date

# Latest standard is 4:0
# https://standard.openownership.org/en/latest/standard/reference.html#record-details-entity


def record_details_person(person):
    return {
            "isComponent": false, //whether person is component of indirect relationship
            "personType": "knownPerson",
            "unspecifiedPersonDetails": {
                "reason": "", //Reason person cannot be specified using codelist
                "description": "", //Additional information in form of String
                },
            "names": [name]
            "identifiers": [person_number],
            "nationalities": [nationality],
            "placeOfBirth": {
                "type": "residence" //codelist
                "postCode": post_code,
                "country": country
                },
            "birthDate": dob, //YYYY, YYY-MM, YYYY-MM-DD
            "deathDate": dob, //YYYY, YYY-MM, YYYY-MM-DD
            "taxResidencies": [], //Array of address objects (see placeOfBirth field)
            "addresses": [] //One or more addresses
            # "politicalExposure": {},
            # politicalExposure/status: isPep/isNotPep
            # politicalExposure/details: array[PEP Status Details ie one or more descriptions
        }



def create_statement(company_number, record_type, record_details: dict):
    """
    A BODS statement consists of an array of Statements containing Record Details (about a person, entity, relationship)

    def create_statement takes a company_number, record_type (string denoting if for person, entity, relationship) and the record_details of said person, entity, relationship). 

    statementId: unique id for this statement. 32-64 characters, String
    statementDate: YYY-MM-DD or date-time format, String
    annotation: Annotations about the document, array[Annotation]
    assertedBy: People or organisations providing info asserted in Statement. Array
    assertedBy/0/name: Name of agent making assertion (so use this for self-declared stuff,
    assertedBy/0/uri An optional URI to identify agent making the assertion
    recordId: Unique id for the record (within publisher's system)
    recordType: Type of record (within publisher's system) to which Statement relates: entiy, person, or relationship
    """
    return {
            "statementId": f"entity-{company_number}",
            "statementDate": str(date.today()),
            "annotations": ["Created by KYBO"],
            "publicationDetails": {
                "publicationDate": str(date.today()),
                "bodsVersion": "4.0",
                "license": "",
                "publisher": {"name": "Know Your Business Owners", url: ""},
                }
            "source":{
                "type": ["officialResearch"],
                "description": "From the UKCH PSC Registry",
                "url": "",
                "retrievedAt": str(date.today()),
                "assertedBy": ["KYBO", "UK Companies House"],
                "assertedBy/0/name": "",
                "assertedBy/0/uri": "",
                },
            "declaration": ""
            "declarationSubject": "",
            "recordID": str(hash(company_number)),
            "recordType": recordType,
            "recordStatus": "new",
            "recordDetails": record_details
            }

