import os
from supabase import create_client, Client


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def register_hospital(
    hospital_name,
    hospital_type,
    phone,
    email,
    address,
    owner_manager_name=None,
    information=None,
):
    hospital = {
        "hospital_name": hospital_name,
        "hospital_type": hospital_type,
        "phone": phone,
        "email": email,
        "address": address,
        "owner_manager_name": owner_manager_name,
        "information": information,
    }

    response = supabase.table("hospitals").insert(hospital).execute()
    return response.data


def register_branch(
    hospital_id,
    branch_name,
    address,
    is_headquarters=False,
    phone=None,
    email=None,
    location=None,
    information=None,
):
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

    response = supabase.table("hospital_branches").insert(branch).execute()
    return response.data
