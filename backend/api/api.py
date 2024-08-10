from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from models.models import Business, Worker, Document, Task, TaskReport
from db_lib import db_client
from auth.security import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter()


def convert_objectid_to_str(document):
    if "_id" in document:
        document["_id"] = str(document["_id"])
    if "business_id" in document:
        document["business_id"] = str(document["business_id"])
    if "user_id" in document:
        document["user_id"] = str(document["user_id"])
    if "reports" in document:
        for report in document["reports"]:
            if "user_id" in report:
                report["user_id"] = str(report["user_id"])
    return document


@router.post("/register_business/")
async def register_business(business: Business):
    client = db_client
    try:
        business_id = await client.create_business(business.name)
        return {"business_id": business_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/register_worker/")
async def register_worker(business_name: str, worker: Worker):
    client = db_client
    try:
        worker_id = await client.add_worker(business_name, worker.dict())
        return {"worker_id": worker_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/documents/")
async def get_documents(business_name: str, current_user: dict = Depends(get_current_user)):
    client = db_client
    try:
        documents = await client.get_documents_by_type(business_name)
        for doc_type, docs in documents.items():
            for doc in docs:
                doc = convert_objectid_to_str(doc)
        return documents
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload_document/")
async def upload_document(business_name: str, file: UploadFile = File(...), description: str = "", doc_type: str = "Unclassified", current_user: dict = Depends(get_current_user)):
    client = db_client
    try:
        business = await client.businesses_collection.find_one({"name": business_name})
        if not business:
            raise HTTPException(
                status_code=400, detail="Business does not exist")

        document_path = f"documents/{file.filename}"
        with open(document_path, "wb") as buffer:
            buffer.write(await file.read())

        document = {
            "name": file.filename,
            "type": doc_type,
            "description": description,
            "file_path": document_path,
            "business_id": business["_id"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "access_control": {
                "financial_director": True,
                "project_manager": True,
                "foreman": True
            }
        }

        document_id = await client.add_document(business_name, document)
        return {"document_id": document_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create_task/")
async def create_task(task: Task, current_user: dict = Depends(get_current_user)):
    client = db_client
    task_info = task.dict()
    task_info["business_id"] = ObjectId(current_user["business_id"])
    try:
        task_id = await client.create_task(task_info)
        return {"task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/")
async def get_tasks(role: str, current_user: dict = Depends(get_current_user)):
    client = db_client
    try:
        tasks = await client.get_tasks_for_role(current_user["business_id"], role)
        for task in tasks:
            task = convert_objectid_to_str(task)
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit_task_report/")
async def submit_task_report(report: TaskReport, current_user: dict = Depends(get_current_user)):
    client = db_client
    try:
        success = await client.submit_task_report(report.task_id, current_user["_id"], report.report)
        if success:
            return {"message": "Report submitted successfully"}
        else:
            raise HTTPException(
                status_code=400, detail="Failed to submit report")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/confirm_task/")
async def confirm_task(task_id: str, current_user: dict = Depends(get_current_user)):
    client = db_client
    try:
        success = await client.confirm_task(task_id)
        if success:
            return {"message": "Task confirmed successfully"}
        else:
            raise HTTPException(
                status_code=400, detail="Failed to confirm task")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reject_task_report/")
async def reject_task_report(task_id: str, current_user: dict = Depends(get_current_user)):
    client = db_client
    try:
        success = await client.reject_task_report(task_id)
        if success:
            return {"message": "Task report rejected successfully"}
        else:
            raise HTTPException(
                status_code=400, detail="Failed to reject task report")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
