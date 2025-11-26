from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from bson import ObjectId
from datetime import datetime
from config.database import db
from config.settings import settings
from routes.auth import get_current_user
from services.model_inference import ModelInference
from services.pdf_generator import PDFGenerator
from services.email_service import EmailService
import os

router = APIRouter()
model_service = ModelInference(settings.MODEL_PATH, settings.CLASSES_PATH)
email_service = EmailService()

@router.post("/analyze")
async def run_analysis(analysis_id: str, user: dict = Depends(get_current_user)):
    analysis_record = await db.db["analyses"].find_one({"_id": ObjectId(analysis_id), "user_id": str(user["_id"])})
    if not analysis_record:
        raise HTTPException(status_code=404, detail="Analysis record not found")
    
    if analysis_record["status"] == "completed":
        return {"message": "Analysis already completed."}

    user_reports_dir = os.path.join(settings.UPLOADS_DIR, user.get("email"), "reports")
    os.makedirs(user_reports_dir, exist_ok=True)
    report_path = os.path.join(user_reports_dir, f"report_{analysis_id}.pdf")

    image_results = []
    all_predictions = []
    
    for image_path in analysis_record["image_paths"]:
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
            
            prediction_result = model_service.predict(image_data)
            image_results.append({"finding": prediction_result["primary_finding"]["class"]})
            all_predictions.extend(prediction_result["predictions"])

        except Exception as e:
            print(f"Error analyzing image {image_path}: {e}")
            raise HTTPException(status_code=500, detail="AI analysis failed")

    # Aggregate results for the PDF
    if all_predictions:
        class_counts = {}
        for pred in all_predictions:
            class_name = pred['class']
            confidence = pred['confidence']
            if class_name not in class_counts:
                class_counts[class_name] = {'count': 0, 'total_confidence': 0.0}
            class_counts[class_name]['count'] += 1
            class_counts[class_name]['total_confidence'] += confidence

        primary_finding_name = None
        max_avg_confidence = -1
        
        for class_name, data in class_counts.items():
            avg_confidence = data['total_confidence'] / data['count']
            if avg_confidence > max_avg_confidence:
                max_avg_confidence = avg_confidence
                primary_finding_name = class_name
        
        additional_findings = []
        for class_name, data in class_counts.items():
            avg_confidence = data['total_confidence'] / data['count']
            if class_name != primary_finding_name and avg_confidence > 0.05: # Using a float threshold
                additional_findings.append({
                    "class": class_name,
                    "confidence": avg_confidence  # Pass as float
                })

        # Corrected: Pass confidence as float, not formatted string
        aggregated_result = {
            "primary_finding": {
                "class": primary_finding_name,
                "confidence": max_avg_confidence  # Pass as float
            },
            "additional_findings": additional_findings
        }
    else:
        raise HTTPException(status_code=500, detail="No predictions generated")

    # Generate PDF
    pdf_generator = PDFGenerator(report_path)
    # The pdf_generator now receives float values and handles formatting internally
    pdf_generator.generate_report(user, {"image_results": image_results, **aggregated_result})

    # Send email
    email_success = email_service.send_report(user["email"], report_path)
    
    # Update analysis record
    await db.db["analyses"].update_one(
        {"_id": ObjectId(analysis_id)},
        {"$set": {
            "status": "completed",
            "results": aggregated_result,
            "report_path": report_path,
            "email_sent": email_success,
            "completed_at": datetime.now()
        }}
    )
    
    return {"message": "Analysis completed, report generated and emailed.", "analysis_id": analysis_id}

@router.get("/results/{analysis_id}")
async def get_analysis_results(analysis_id: str, user: dict = Depends(get_current_user)):
    analysis_record = await db.db["analyses"].find_one({"_id": ObjectId(analysis_id), "user_id": str(user["_id"])})
    if not analysis_record:
        raise HTTPException(status_code=404, detail="Analysis record not found")
        
    analysis_record["_id"] = str(analysis_record["_id"])
    return analysis_record

@router.get("/history")
async def get_user_history(user: dict = Depends(get_current_user)):
    history = await db.db["analyses"].find({"user_id": str(user["_id"])}).to_list(100)
    for record in history:
        record["_id"] = str(record["_id"])
    return history

@router.get("/reports/{analysis_id}")
async def download_report(analysis_id: str, user: dict = Depends(get_current_user)):
    analysis_record = await db.db["analyses"].find_one({"_id": ObjectId(analysis_id), "user_id": str(user["_id"]), "report_path": {"$exists": True}})
    if not analysis_record:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report_path = analysis_record["report_path"]
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    return FileResponse(path=report_path, filename=os.path.basename(report_path), media_type="application/pdf")