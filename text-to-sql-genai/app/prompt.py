import json

# --------------------------------------------------
# Static schema description
# --------------------------------------------------
SCHEMA_DESCRIPTION = """
You are a SQL assistant for a healthcare analytics database.

Database: Databricks
Catalog: healthcare
Schema: hmis
"""

# --------------------------------------------------
# Table column definitions (prevents hallucinations)
# --------------------------------------------------
TABLE_COLUMNS = {
    "admission": [
        "admission_id",
        "admission_date",
        "discharge_date",
        "admission_type",
        "admission_status",
        "patient_id",
        "department_id",
        "ward_id",
        "bed_id",
        "disease_id"
    ],
    "bed": [
        "bed_id",
        "bed_number",
        "bed_status",
        "ward_id"
    ],
    "billing": [
        "bill_id",
        "bill_date",
        "total_amount",
        "insurance_covered_amount",
        "patient_payable_amount",
        "payment_status",
        "payment_mode",
        "admission_id"
    ],
    "billing_detail": [
        "billing_detail_id",
        "charge_type",
        "reference_id",
        "amount",
        "bill_id"
    ],
    "department": [
        "department_id",
        "department_name",
        "department_type",
        "floor_number",
        "status"
    ],
    "diagnostic_test": [
        "test_id",
        "test_name",
        "test_category",
        "standard_cost",
        "department_id"
    ],
    "disease": [
        "disease_id",
        "disease_name",
        "disease_category"
    ],
    "doctor": [
        "doctor_id",
        "employee_id",
        "specialization",
        "qualification",
        "experience_years"
    ],
    "drug": [
        "drug_id",
        "drug_name",
        "brand_name",
        "drug_category",
        "unit_cost",
        "manufacturer_id"
    ],
    "drug_inventory": [
        "inventory_id",
        "current_stock",
        "reorder_level",
        "inventory_status",
        "last_restock_date",
        "drug_id"
    ],
    "drug_manufacturer": [
        "manufacturer_id",
        "manufacturer_name",
        "country",
        "reliability_rating",
        "contract_status"
    ],
    "employee": [
        "employee_id",
        "employee_name",
        "gender",
        "role",
        "employment_type",
        "date_of_joining",
        "department_id"
    ],
    "insurance_provider": [
        "insurance_provider_id",
        "provider_name",
        "provider_type",
        "contact_details",
        "coverage_limit"
    ],
    "patient": [
        "patient_id",
        "gender",
        "date_of_birth",
        "blood_group",
        "city",
        "contact_number"
    ],
    "patient_diagnostic": [
        "patient_diagnostic_id",
        "test_date",
        "result_status",
        "admission_id",
        "test_id",
        "doctor_id"
    ],
    "patient_insurance": [
        "patient_insurance_id",
        "policy_number",
        "coverage_percentage",
        "policy_start_date",
        "policy_end_date",
        "patient_id",
        "insurance_provider_id"
    ],
    "prescription": [
        "prescription_id",
        "dosage",
        "frequency",
        "duration_days",
        "admission_id",
        "drug_id"
    ],
    "staff_assignment": [
        "assignment_id",
        "employee_id",
        "ward_id",
        "shift"
    ],
    "ward": [
        "ward_id",
        "ward_name",
        "ward_type",
        "total_beds",
        "department_id"
    ]
}

# --------------------------------------------------
# JSON join graph
# --------------------------------------------------
JOIN_GRAPH = {
    "relationships": [
        {"from": "admission.patient_id", "to": "patient.patient_id"},
        {"from": "admission.department_id", "to": "department.department_id"},
        {"from": "admission.ward_id", "to": "ward.ward_id"},
        {"from": "admission.bed_id", "to": "bed.bed_id"},
        {"from": "admission.disease_id", "to": "disease.disease_id"},

        {"from": "billing.admission_id", "to": "admission.admission_id"},
        {"from": "billing_detail.bill_id", "to": "billing.bill_id"},

        {"from": "patient_diagnostic.admission_id", "to": "admission.admission_id"},
        {"from": "patient_diagnostic.test_id", "to": "diagnostic_test.test_id"},
        {"from": "patient_diagnostic.doctor_id", "to": "doctor.doctor_id"},

        {"from": "doctor.employee_id", "to": "employee.employee_id"},
        {"from": "employee.department_id", "to": "department.department_id"},

        {"from": "prescription.admission_id", "to": "admission.admission_id"},
        {"from": "prescription.drug_id", "to": "drug.drug_id"},

        {"from": "drug.manufacturer_id", "to": "drug_manufacturer.manufacturer_id"},
        {"from": "drug_inventory.drug_id", "to": "drug.drug_id"},

        {"from": "ward.department_id", "to": "department.department_id"},
        {"from": "bed.ward_id", "to": "ward.ward_id"},

        {"from": "patient_insurance.patient_id", "to": "patient.patient_id"},
        {"from": "patient_insurance.insurance_provider_id", "to": "insurance_provider.insurance_provider_id"},

        {"from": "staff_assignment.employee_id", "to": "employee.employee_id"},
        {"from": "staff_assignment.ward_id", "to": "ward.ward_id"}
    ],

    "join_paths": [
        "patient → admission",
        "patient → admission → billing",
        "patient → admission → billing → billing_detail",
        "patient → admission → prescription → drug",
        "patient → admission → patient_diagnostic",

        "admission → billing",
        "admission → billing → billing_detail",
        "admission → prescription → drug",
        "admission → disease",
        "admission → ward",
        "admission → bed",

        "doctor → patient_diagnostic → admission",

        "department → admission",
        "department → ward → admission",
        "department → employee → doctor → patient_diagnostic → admission",

        "ward → admission",
        "ward → bed → admission",

        "employee → department → admission",

        "patient → patient_insurance → insurance_provider"
    ]
}

# --------------------------------------------------
# SQL generation rules
# --------------------------------------------------
SQL_RULES = """
SQL Rules:
- Only generate SELECT queries
- Do not use DELETE, UPDATE, INSERT, DROP, ALTER, or TRUNCATE
- Use fully qualified table names: healthcare.hmis.table_name
- Use table aliases when joining
- Always follow the join paths provided
- Do not invent new relationships
- Do not invent columns
- Doctor name is stored in employee.employee_name
- Return only SQL, no explanation
"""

# --------------------------------------------------
# Prompt builder
# --------------------------------------------------
def build_prompt(user_question: str) -> str:
    join_graph_text = json.dumps(JOIN_GRAPH, indent=2)

    # Build column section
    column_text = "Table Columns:\n"
    for table, cols in TABLE_COLUMNS.items():
        column_text += f"{table}: {', '.join(cols)}\n"

    prompt = f"""
{SCHEMA_DESCRIPTION}

{column_text}

Join Graph (JSON):
{join_graph_text}

{SQL_RULES}

User question: {user_question}
"""

    return prompt
