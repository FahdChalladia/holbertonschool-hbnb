import uuid
from datetime import datetime

class User:
    """Modèle utilisateur pour HBnB"""
    
    def __init__(self, *args, **kwargs):
        """Initialisation avec génération automatique des timestamps"""
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
        
        # Attributs spécifiques à User
        self.email = kwargs.get('email', '')
        self.password = kwargs.get('password', '')  # Note: Devrait être hashé en production
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        
        # Gestion des arguments supplémentaires
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)

    def save(self):
        """Met à jour le timestamp updated_at"""
        self.updated_at = datetime.now()
        return self

    def update(self, data):
        """Met à jour les attributs avec les nouvelles données"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.save()
        return self

    def to_dict(self):
        """Convertit l'instance en dictionnaire pour sérialisation"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            '__class__': self.__class__.__name__
        }

    def __str__(self):
        """Représentation textuelle de l'utilisateur"""
        return f"[User] ({self.id}) {self.__dict__}"
