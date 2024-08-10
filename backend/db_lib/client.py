from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from datetime import datetime
import bcrypt


class MongoDBClient:
    def __init__(self, uri: str, database: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[database]
        self.businesses_collection = self.db['businesses']
        self.users_collection = self.db['users']
        self.documents_collection = self.db['documents']
        self.financial_operations_collection = self.db['financial_operations']
        self.financial_reports_collection = self.db['financial_reports']
        self.tasks_collection = self.db['tasks']

    async def create_business(self, name: str):
        existing_business = await self.businesses_collection.find_one({"name": name})
        if existing_business:
            raise ValueError("Business already exists")

        business = {
            "name": name,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "documents": [],
            "employees": []
        }

        result = await self.businesses_collection.insert_one(business)
        return str(result.inserted_id)

    async def add_worker(self, business_name: str, worker_info: dict):
        business = await self.businesses_collection.find_one({"name": business_name})
        if not business:
            raise ValueError("Business does not exist")

        existing_worker = await self.users_collection.find_one({
            "phone_number": worker_info["phone_number"],
            "business_id": business["_id"]
        })
        if existing_worker:
            raise ValueError(
                "Worker with this phone number already exists in this business")

        password_hash = bcrypt.hashpw(
            worker_info["password"].encode('utf-8'), bcrypt.gensalt())
        worker_info["password_hash"] = password_hash
        worker_info["business_id"] = business["_id"]
        worker_info["created_at"] = datetime.utcnow()
        worker_info["updated_at"] = datetime.utcnow()
        del worker_info["password"]

        result = await self.users_collection.insert_one(worker_info)

        await self.businesses_collection.update_one(
            {"_id": business["_id"]},
            {"$push": {"employees": result.inserted_id}}
        )

        return str(result.inserted_id)

    async def add_document(self, business_name: str, document: dict):
        business = await self.businesses_collection.find_one({"name": business_name})
        if not business:
            raise ValueError("Business does not exist")

        document["business_id"] = business["_id"]
        document["created_at"] = datetime.utcnow()
        document["updated_at"] = datetime.utcnow()

        result = await self.documents_collection.insert_one(document)

        await self.businesses_collection.update_one(
            {"_id": business["_id"]},
            {"$push": {"documents": result.inserted_id}}
        )

        return str(result.inserted_id)

    async def get_documents_by_type(self, business_name: str):
        business = await self.businesses_collection.find_one({"name": business_name})
        if not business:
            raise ValueError("Business does not exist")

        documents = await self.documents_collection.find({"business_id": business["_id"]}).to_list(length=None)
        classified_docs = {}
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            doc["business_id"] = str(doc["business_id"])
            doc_type = doc.get("type", "Unclassified")
            if doc_type not in classified_docs:
                classified_docs[doc_type] = []
            classified_docs[doc_type].append(doc)

        return classified_docs

    async def authenticate_user(self, phone_number: str, password: str):
        user = await self.users_collection.find_one({"phone_number": phone_number})
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password_hash"]):
            return user
        return None

    async def get_businesses_for_user(self, user_id: ObjectId):
        businesses = await self.businesses_collection.find({"employees": user_id}).to_list(length=None)
        for business in businesses:
            business["_id"] = str(business["_id"])
        return businesses

    async def get_user_by_phone_number(self, phone_number: str):
        user = await self.users_collection.find_one({"phone_number": phone_number})
        if user:
            user["_id"] = str(user["_id"])
        return user

    async def create_task(self, task_info: dict):
        task_info["created_at"] = datetime.utcnow()
        task_info["updated_at"] = datetime.utcnow()
        task_info["status"] = "pending"
        task_info["reports"] = []

        result = await self.tasks_collection.insert_one(task_info)
        return str(result.inserted_id)

    async def get_tasks_for_role(self, business_id: str, role: str):
        tasks = await self.tasks_collection.find({"business_id": ObjectId(business_id), "role": role, "status": "pending"}).to_list(length=None)
        for task in tasks:
            task["_id"] = str(task["_id"])
            task["business_id"] = str(task["business_id"])
        return tasks

    async def submit_task_report(self, task_id: str, user_id: str, report: str):
        report_info = {
            "user_id": ObjectId(user_id),
            "report": report,
            "created_at": datetime.utcnow()
        }
        result = await self.tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$push": {"reports": report_info}}
        )
        return result.modified_count > 0

    async def confirm_task(self, task_id: str):
        result = await self.tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"status": "confirmed"}}
        )
        return result.modified_count > 0

    async def reject_task_report(self, task_id: str):
        result = await self.tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"reports": [], "status": "pending"}}
        )
        return result.modified_count > 0
