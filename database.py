import os
from supabase import create_client, Client


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


def register_hospital(
    access_token,
    refresh_token,
    hospital_name,
    hospital_type,
    phone,
    email,
    address,
    owner_manager_name=None,
    information=None,
):
    client = authenticated_client(access_token, refresh_token)

    response = client.rpc(
        "register_hospital_with_owner",
        {
            "p_hospital_name": hospital_name,
            "p_hospital_type": hospital_type,
            "p_phone": phone,
            "p_email": email,
            "p_address": address,
            "p_owner_manager_name": owner_manager_name,
            "p_information": information,
        },
    ).execute()

    return response.data


def register_branch(
    access_token,
    refresh_token,
    hospital_id,
    branch_name,
    address,
    is_headquarters=False,
    phone=None,
    email=None,
    location=None,
    information=None,
):
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

    response = client.table("hospital_branches").insert(branch).execute()
    return response.data


def register_department(
    access_token,
    refresh_token,
    branch_id,
    department_name,
    department_type,
    description=None,
):
    client = authenticated_client(access_token, refresh_token)

    department = {
        "branch_id": branch_id,
        "department_name": department_name,
        "department_type": department_type,
        "description": description,
    }

    response = client.table("departments").insert(department).execute()
    return response.data


def get_user_memberships(access_token, refresh_token):
    client = authenticated_client(access_token, refresh_token)
    response = (
        client.table("hospital_users")
        .select("hospital_id, role, hospitals(hospital_name)")
        .execute()
    )
    return response.data
