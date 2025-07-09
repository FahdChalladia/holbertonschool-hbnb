from flask_restx import Namespace, Resource
from app.services.facade import HBNBFacade

api = Namespace('Users', description='Opérations utilisateurs')

facade = HBNBFacade()

@api.route('/')
class UserList(Resource):
    def get(self):
        """Liste tous les utilisateurs"""
        users = facade.user_repo.get_all()
        return [u.to_dict() for u in users]
    
    def post(self):
        """Crée un nouvel utilisateur"""
        data = api.payload
        user = facade.create_user(data)
        return user.to_dict(), 201

@api.route('/<string:user_id>')
class UserDetail(Resource):
    def get(self, user_id):
        """Récupère un utilisateur spécifique"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "Utilisateur non trouvé")
        return user.to_dict()
