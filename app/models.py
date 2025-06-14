from bson.objectid import ObjectId

class User:
    def __init__(self, db):
        self.collection = db.users

    def create(self, name, email, password, is_employee=False):
        if self.collection.find_one({"email": email}):
            return None
            
        user_data = {
            "name": name,
            "email": email,
            "password": password,
            "is_employee": is_employee,
            "borrowed_books": []
        }
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)

    def find_by_email(self, email):
        return self.collection.find_one({"email": email})

    def authenticate(self, email, password):
        user = self.find_by_email(email)
        if user and user["password"] == password:
            return user
        return None

    def update(self, user_id, updates):
        updates.pop('_id', None)
        updates.pop('is_employee', None)
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updates}
        )
        return result.modified_count

    def delete(self, user_id):
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count

    def list_all(self, employees_only=False):
        query = {"is_employee": True} if employees_only else {}
        return list(self.collection.find(query))