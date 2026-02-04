from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_supabase
from app.config import settings

security = HTTPBearer()

async def verify_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT and check admin access."""
    token = credentials.credentials
    supabase = get_supabase()
    
    try:
        user = supabase.auth.get_user(token)
        
        if not user or not user.user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        if user.user.email != settings.ADMIN_EMAIL:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not admin")
        
        return user.user
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

