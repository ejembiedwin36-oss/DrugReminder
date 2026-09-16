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
