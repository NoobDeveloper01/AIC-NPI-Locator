import requests
import json
import pandas as pd
from config import API_URL

def get_npi_details(npi_id):
    try:
        response = requests.get(API_URL.format(npi_id))
        response.raise_for_status()
        data = response.json()
        if "result_count" in data and data["result_count"] > 0:
            return data["results"][0]
        else:
            return {"NPI ID": npi_id, "Status": "Not Found"}
    except requests.exceptions.RequestException as e:
        return {"NPI ID": npi_id, "Status": f"Error: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"NPI ID": npi_id, "Status": "Error: Invalid response format"}


def blank_npi_data(npi_data):
    parsed_data = {
        "NPI ID": npi_data.get("NPI ID", ""),
        "First Name": npi_data.get("basic", {}).get("first_name", ""),
        "Last Name": npi_data.get("basic", {}).get("last_name", ""),
        "Middle Name": npi_data.get("basic", {}).get("middle_name", ""),
        "Credential": npi_data.get("basic", {}).get("credential", ""),
        "Sole Proprietor": npi_data.get("basic", {}).get("sole_proprietor", ""),
        "Gender": npi_data.get("basic", {}).get("gender", ""),
        "Enumeration Date": npi_data.get("basic", {}).get("enumeration_date", ""),
        "Last Updated": npi_data.get("basic", {}).get("last_updated", ""),
        "Certification Date": npi_data.get("basic", {}).get("certification_date", ""),
        "Status": npi_data.get("basic", {}).get("status", ""),
        "Enumeration Type": npi_data.get("enumeration_type", ""),
    }

    # Process addresses
    addresses = npi_data.get("addresses", [])
    for i, address in enumerate(addresses):
        prefix = f"Address_{i+1}_"
        parsed_data.update({
            f"{prefix}Purpose": address.get("address_purpose", ""),
            f"{prefix}Type": address.get("address_type", ""),
            f"{prefix}Address1": address.get("address_1", ""),
            f"{prefix}Address2": address.get("address_2", ""),
            f"{prefix}City": address.get("city", ""),
            f"{prefix}State": address.get("state", ""),
            f"{prefix}Postal Code": address.get("postal_code", ""),
            f"{prefix}Telephone": address.get("telephone_number", ""),
            f"{prefix}Fax": address.get("fax_number", ""),
        })

    # Process practice locations
    practice_locations = npi_data.get("practiceLocations", [])
    for i, location in enumerate(practice_locations):
        prefix = f"PracticeLocation_{i+1}_"
        parsed_data.update({
            f"{prefix}Address1": location.get("address_1", ""),
            f"{prefix}City": location.get("city", ""),
            f"{prefix}State": location.get("state", ""),
            f"{prefix}Postal Code": location.get("postal_code", ""),
            f"{prefix}Telephone": location.get("telephone_number", ""),
            f"{prefix}Fax": location.get("fax_number", ""),
        })

    # Process taxonomies
    taxonomies = npi_data.get("taxonomies", [])
    for i, taxonomy in enumerate(taxonomies):
        prefix = f"Taxonomy_{i+1}_"
        parsed_data.update({
            f"{prefix}Code": taxonomy.get("code", ""),
            f"{prefix}Description": taxonomy.get("desc", ""),
            f"{prefix}State": taxonomy.get("state", ""),
            f"{prefix}License": taxonomy.get("license", ""),
            f"{prefix}Primary": str(taxonomy.get("primary", "")),
        })

    # Process identifiers
    identifiers = npi_data.get("identifiers", [])
    for i, identifier in enumerate(identifiers):
        prefix = f"Identifier_{i+1}_"
        parsed_data.update({
            f"{prefix}Code": identifier.get("code", ""),
            f"{prefix}Description": identifier.get("desc", ""),
            f"{prefix}Identifier": identifier.get("identifier", ""),
            f"{prefix}State": identifier.get("state", ""),
        })

    parsed_data["Status"] = "Found" if npi_data.get("number", "") else "Not Found"

    return pd.DataFrame([parsed_data])

def parse_npi_data(npi_data):
    parsed_data = {
        "NPI ID": npi_data.get("number", ""),
        "First Name": npi_data.get("basic", {}).get("first_name", ""),
        "Last Name": npi_data.get("basic", {}).get("last_name", ""),
        "Middle Name": npi_data.get("basic", {}).get("middle_name", ""),
        "Credential": npi_data.get("basic", {}).get("credential", ""),
        "Sole Proprietor": npi_data.get("basic", {}).get("sole_proprietor", ""),
        "Gender": npi_data.get("basic", {}).get("gender", ""),
        "Enumeration Date": npi_data.get("basic", {}).get("enumeration_date", ""),
        "Last Updated": npi_data.get("basic", {}).get("last_updated", ""),
        "Certification Date": npi_data.get("basic", {}).get("certification_date", ""),
        "Status": npi_data.get("basic", {}).get("status", ""),
        "Enumeration Type": npi_data.get("enumeration_type", ""),
    }

    # Process addresses
    addresses = npi_data.get("addresses", [])
    for i, address in enumerate(addresses):
        prefix = f"Address_{i+1}_"
        parsed_data.update({
            f"{prefix}Purpose": address.get("address_purpose", ""),
            f"{prefix}Type": address.get("address_type", ""),
            f"{prefix}Address1": address.get("address_1", ""),
            f"{prefix}Address2": address.get("address_2", ""),
            f"{prefix}City": address.get("city", ""),
            f"{prefix}State": address.get("state", ""),
            f"{prefix}Postal Code": address.get("postal_code", ""),
            f"{prefix}Telephone": address.get("telephone_number", ""),
            f"{prefix}Fax": address.get("fax_number", ""),
        })

    # Process practice locations
    practice_locations = npi_data.get("practiceLocations", [])
    for i, location in enumerate(practice_locations):
        prefix = f"PracticeLocation_{i+1}_"
        parsed_data.update({
            f"{prefix}Address1": location.get("address_1", ""),
            f"{prefix}City": location.get("city", ""),
            f"{prefix}State": location.get("state", ""),
            f"{prefix}Postal Code": location.get("postal_code", ""),
            f"{prefix}Telephone": location.get("telephone_number", ""),
            f"{prefix}Fax": location.get("fax_number", ""),
        })

    # Process taxonomies
    taxonomies = npi_data.get("taxonomies", [])
    for i, taxonomy in enumerate(taxonomies):
        prefix = f"Taxonomy_{i+1}_"
        parsed_data.update({
            f"{prefix}Code": taxonomy.get("code", ""),
            f"{prefix}Description": taxonomy.get("desc", ""),
            f"{prefix}State": taxonomy.get("state", ""),
            f"{prefix}License": taxonomy.get("license", ""),
            f"{prefix}Primary": str(taxonomy.get("primary", "")),
        })

    # Process identifiers
    identifiers = npi_data.get("identifiers", [])
    for i, identifier in enumerate(identifiers):
        prefix = f"Identifier_{i+1}_"
        parsed_data.update({
            f"{prefix}Code": identifier.get("code", ""),
            f"{prefix}Description": identifier.get("desc", ""),
            f"{prefix}Identifier": identifier.get("identifier", ""),
            f"{prefix}State": identifier.get("state", ""),
        })

    parsed_data["Status"] = "Found" if parsed_data["NPI ID"] else "Not Found"

    return pd.DataFrame([parsed_data])