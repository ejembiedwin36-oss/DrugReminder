import os

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def authenticated_client(access_token, refresh_token):
    """Create a Supabase client using the current user's session."""
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    client.auth.set_session(access_token, refresh_token)
    return client


def sign_up(email, password):
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return client.auth.sign_up({"email": email, "password": password})


def sign_in(email, password):
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return client.auth.sign_in_with_password({"email": email, "password": password})


def register_hospital(access_token, refresh_token, hospital_name, hospital_type, phone, email, address, owner_manager_name=None, information=None):
    client = authenticated_client(access_token, refresh_token)
    response = client.rpc("register_hospital_with_owner", {
        "p_hospital_name": hospital_name,
        "p_hospital_type": hospital_type,
        "p_phone": phone,
        "p_email": email,
        "p_address": address,
        "p_owner_manager_name": owner_manager_name,
        "p_information": information,
    }).execute()
    return response.data


def register_branch(access_token, refresh_token, hospital_id, branch_name, address, is_headquarters=False, phone=None, email=None, location=None, information=None):
    client = authenticated_client(access_token, refresh_token)
    branch = {
        "hospital_id": hospital_id,
        "branch_name": branch_name,
        "is_headquarters": is_headquarters,
        "phone": phone,
        "email": email,
        "address": address,
        "location": location,
        "information": information,
    }
    return client.table("hospital_branches").insert(branch).execute().data


def register_department(access_token, refresh_token, branch_id, department_name, department_type, description=None):
    client = authenticated_client(access_token, refresh_token)
    department = {
        "branch_id": branch_id,
        "department_name": department_name,
        "department_type": department_type,
        "description": description,
    }
    return client.table("departments").insert(department).execute().data


def get_user_memberships(access_token, refresh_token):
    client = authenticated_client(access_token, refresh_token)
    return client.table("hospital_users").select("hospital_id, role, hospitals(hospital_name)").execute().data


def get_hospital_branches(access_token, refresh_token, hospital_id):
    client = authenticated_client(access_token, refresh_token)
    return client.table("hospital_branches").select("id, branch_name").eq("hospital_id", hospital_id).order("branch_name").execute().data


def get_branch_departments(access_token, refresh_token, branch_id):
    client = authenticated_client(access_token, refresh_token)
    return client.table("departments").select("id, department_name, department_type").eq("branch_id", branch_id).order("department_name").execute().data


def register_staff(access_token, refresh_token, hospital_id, branch_id, department_id, full_name, staff_id, role, phone=None, email=None, address=None):
    client = authenticated_client(access_token, refresh_token)
    staff = {
        "hospital_id": hospital_id,
        "branch_id": branch_id,
        "department_id": department_id,
        "full_name": full_name,
        "staff_id": staff_id,
        "role": role,
        "phone": phone,
        "email": email,
        "address": address,
    }
    return client.table("staff").insert(staff).execute().data


def create_staff_assignment(access_token, refresh_token, staff_id, hospital_id, branch_id, department_id, role):
    client = authenticated_client(access_token, refresh_token)
    assignment = {
        "staff_id": staff_id,
        "hospital_id": hospital_id,
        "branch_id": branch_id,
        "department_id": department_id,
        "role": role,
    }
    return client.table("staff_assignments").insert(assignment).execute().data


def get_hospital_staff(access_token, refresh_token, hospital_id):
    """Get all staff belonging to one hospital with branch and department names."""
    client = authenticated_client(access_token, refresh_token)
    response = (
        client.table("staff")
        .select(
            "id, full_name, staff_id, role, phone, email, is_active, "
            "hospital_branches!staff_branch_id_fkey(branch_name), "
            "departments!staff_department_id_fkey(department_name)"
        )
        .eq("hospital_id", hospital_id)
        .order("full_name")
        .execute()
    )
    return response.data


def get_staff_member(access_token, refresh_token, hospital_id, staff_record_id):
    """Get one staff member while keeping the query inside the requested hospital."""
    client = authenticated_client(access_token, refresh_token)
    response = (
        client.table("staff")
        .select(
            "id, hospital_id, branch_id, department_id, full_name, staff_id, role, phone, email, address, "
            "is_active, created_at, hospital_branches!staff_branch_id_fkey(branch_name), "
            "departments!staff_department_id_fkey(department_name)"
        )
        .eq("hospital_id", hospital_id)
        .eq("id", staff_record_id)
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None


def get_staff_assignment_history(access_token, refresh_token, hospital_id, staff_record_id):
    """Get the current and previous branch/department assignments for one staff member."""
    client = authenticated_client(access_token, refresh_token)
    response = (
        client.table("staff_assignments")
        .select(
            "id, role, started_at, ended_at, transfer_reason, "
            "hospital_branches(branch_name), departments(department_name)"
        )
        .eq("hospital_id", hospital_id)
        .eq("staff_id", staff_record_id)
        .order("started_at", desc=True)
        .execute()
    )
    return response.data


def transfer_staff(access_token, refresh_token, staff_record_id, branch_id, department_id, role, transfer_reason):
    """Transfer a staff member atomically through the secure database function."""
    client = authenticated_client(access_token, refresh_token)
    return client.rpc("transfer_staff", {
        "p_staff_id": staff_record_id,
        "p_branch_id": branch_id,
        "p_department_id": department_id,
        "p_role": role,
        "p_transfer_reason": transfer_reason,
    }).execute().data


def register_patient(access_token, refresh_token, hospital_id, branch_id, patient_number, full_name, date_of_birth=None, phone=None, email=None, address=None):
    """Register a patient and initial branch-history record atomically."""
    client = authenticated_client(access_token, refresh_token)
    return client.rpc("register_patient", {
        "p_hospital_id": hospital_id,
        "p_branch_id": branch_id,
        "p_patient_number": patient_number,
        "p_full_name": full_name,
        "p_date_of_birth": date_of_birth or None,
        "p_phone": phone,
        "p_email": email,
        "p_address": address,
    }).execute().data
