from supabase import create_client, Client
from app.core.config import settings

# Global client with anon key for public operations
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def get_supabase_client(access_token: str = None) -> Client:
    """
    Get a Supabase client with optional user access token for RLS.
    If access_token is provided, it will be used for authenticated requests.
    """
    if access_token:
        # Create a client with the user's JWT token for RLS
        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        client.auth.set_session(access_token, access_token)  # Set the user's token
        return client
    return supabase


