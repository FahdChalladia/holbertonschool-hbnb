from typing import List, Optional
from app.models.user import User

class HBNBFacade:
    # ... existing code ...
    
    def get_all_users(self) -> List[User]:
        """Get all users without sensitive data"""
        users = self.repository.get_all_users()
        # Ensure passwords are never returned
        for user in users:
            if hasattr(user, 'password'):
                delattr(user, 'password')
        return users
    
    def update_user(self, user_id: str, update_data: dict) -> User:
        """Update user with validation"""
        user = self.repository.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Validate email if being updated
        if 'email' in update_data:
            existing = self.repository.get_user_by_email(update_data['email'])
            if existing and existing.id != user_id:
                raise ValueError("Email already in use")
        
        user.update(**update_data)
        self.repository.save_user(user)
        return user
        