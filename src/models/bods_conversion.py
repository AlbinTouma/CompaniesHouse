import json
import uuid
from datetime import date
from pydantic import BaseModel

# Latest standard is 4:0
# https://standard.openownership.org/en/latest/standard/reference.html#record-details-entity


#Reason is a codelist
class unSpecifiedPersonDetails(BaseModel):
    reason: str
    description: str


class Names(BaseModel):
    type: str | None = "legal"
    fullName: str
    givenName: str | None //same as first name
    familyName: str | None


class Country(BaseModel):
    name: str | None = "United Kingdom"
    code: str | None = "GB"


class Addresses(BaseModel):
    type: str | None = "service"
    address: str | None
    postCode: str | None
    country: Country


class RecordPerson(BaseModel):
    isComponent: bool | None = false
    personType: str | None  = "knownPerson"
    unSpecifiedPersonDetails: unSpecifiedPersonDetails | None
    names: Names
    birthDate: str  //YYYY-MM-DD
    addresses: Addresses


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
        }



def record_details_entity(company):
    """
        entityType: The form of the entity described in the statement"
    """

    return {
            "isComponent": false, //whether person is component of indirect relationship
            "entityType": company.type,
            "entityType/type": "registeredEntity", //different codes, need mapping in future
            "entityType/subtype": "other", //Type must align with entity type!!
            "entityType/details": "", //Provide local name for type of entity ie Ministerium for dep
            "unspecifiedEntityDetails": "", //explanation of why entity anonymous
            "name": company.full_name, //string
            "alternateNames": [], //aray of strings, names
            "jurisdiction": {
                "name": company.country,
                "code": "gb", //2 letter ISO code for jurisdiction
                },
            "identifiers": {
                "id": company.company_number,
                "scheme": "GB-COH", //for person it is PASSPORT, TAXID, IDCARD
                "schemeName":, "UK Companies House",
                "uri": "https://www.ukch.com/",
                },
            "foundingDate": "", //YYYY-MM-DD format. 
            "dissolutionDate": "", //YYY-MM-DD
            "addresses": {
                "type": "registered", // code function of address
                "postCode": company.postCode,
                "country": company.country,
                }, 
            "uri": "",
            }

def record_details_relationship(entity, component_records: list, owner_id, interests: list[interests]){
     return {
            "isComponent": false, //whether person is component of indirect relationship
            "componentRecords": component_records,
            "subject": recordId, //recordId for interested party in the relationship ie person / company number
            "interestedParty": owner_id , //id of the owner
            "interests": interests, //list[Interest dicts]
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
                "bodsVersion": "0.4",
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

