import uuid
import json
from typing import List, Dict, Any
from ast import literal_eval

"""
General
The format of the data presented to the tool:

MUST be a valid JSON array of objects
is presumed to be BODS 0.4-like, unless the first object in the JSON array has a publicationDetails.bodsVersion value of '0.2' or '0.3', in which case all objects will be presumed to be BODS 0.2/0.3-like.
is presumed to have a time dimension (that is to show the properties of people, entities and relationships changing over a period of time) if:
In BODS 0.2 or 0.3-like data, the replacesStatements field is present in any object and contains a value corresponding to the statementID value of a different object (both objects having the same statementType value).
In BODS 0.4-like data, there are multiple objects which share both a recordId value and a recordType value.
The list of JSON objects presented to the tool is first filtered to represent a snapshot in time (if the data has a time dimension). Then it is processed to draw person nodes, entity nodes and relationship edges.

"""

class BODS_MAPPER:
    """
    Maps UK Companies House data (company, officers, PSCs)
    into Beneficial Ownership Data Standard (BODS) JSON.
    """

    def __init__(self, companies: List[Dict[str, Any]], pscs: List[Dict[str, Any]], officers: List[Dict[str, Any]]):
        self.companies = companies
        self.pscs = pscs
        self.officers = officers
        self.statements = []
        self.entity_ids = set()
        self.person_ids = set()

    def _make_entity_id(self, company_number: str) -> str:
        return f"entity-{company_number}"

    def _make_person_id(self, name: str) -> str:
        safe_name = name.lower().strip().replace(" ", "-").replace(".", "")
        return f"person-{safe_name}"

    def _add_entity_statement(self, company: Dict[str, Any]):
        entity_id = self._make_entity_id(company["company_number"])
        if entity_id in self.entity_ids:
            return
        self.entity_ids.add(entity_id)

        statement = {
            "statementID": entity_id,
            "statementType": "entityStatement",
            "entityType": "registeredEntity",
            "names": [company["company_name"]],
            "identifiers": [{"scheme": "GB-COH", "id": company["company_number"]}],
            "addresses": [{"type": "registered", "address": company["full_address"]}],
            "source": {"type": "officialRegister", "description": "UK Companies House"}
        }
        self.statements.append(statement)

    def _add_person_statement(self, name: str, source_desc: str) -> str:
        person_id = self._make_person_id(name)
        if person_id in self.person_ids:
            return person_id
        self.person_ids.add(person_id)

        statement = {
            "statementID": person_id,
            "statementType": "personStatement",
            "personType": "knownPerson",
            "names": [name],
            "source": {"type": "officialRegister", "description": source_desc}
        }
        self.statements.append(statement)
        return person_id

    def _add_ownership_statement(self, company_id: str, person_id: str, details: List[str], beneficial=True, relationship_type="shareholding"):

        if isinstance(details, str):
            try:
                details = literal_eval(details)
            except Exception:
                details = [details]
        elif not isinstance(details, list):
            details = [str(details)]

        statement = {
            "statementID": f"{relationship_type}-{uuid.uuid4()}",
            "statementType": "ownershipOrControlStatement",
            "subject": {"describedByEntityStatement": company_id},
            "interestedParty": {"describedByPersonStatement": person_id},
            "interests": [{
                "type": relationship_type,
                "details": literal_eval(details),
                "beneficialOwnershipOrControl": beneficial
            }],
            "source": {"type": "officialRegister", "description": "UK Companies House"}
        }
        self.statements.append(statement)

    def map(self) -> Dict[str, Any]:
        # --- 1️⃣ Companies
        for c in self.companies:
            if not c.get("company_number"):
                continue
            self._add_entity_statement(c)

        for p in self.pscs:
            if not p.get("full_name"):
                continue
            person_id = self._add_person_statement(p["full_name"], "UK Companies House PSC Register")
            company_id = self._make_entity_id(p["company_number"])
            self._add_ownership_statement(
                company_id,
                person_id,
                p.get("natures_of_control", []),
                beneficial=True,
                relationship_type="shareholding"
            )

        for o in self.officers:
            if not o.get("full_name"):
                continue
            person_id = self._add_person_statement(o["full_name"], "UK Companies House Officers Register")
            company_id = self._make_entity_id(o["company_number"])
            self._add_ownership_statement(
                company_id,
                person_id,
                [o.get("role", "officer")],
                beneficial=False,
                relationship_type="controlViaPosition"
            )

        return {"statements": self.statements}

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.map(), indent=indent)

