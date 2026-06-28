from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.candidate import Candidate
from app.models.job import JobDescription
from app.elasticsearch_client import index_candidate, search_candidates

import sys
import os

# To allow importing ml_engine modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from ml_engine.preprocessing import extract_text_from_pdf, extract_sections, extract_jd_features, extract_email, extract_phone, extract_total_experience
from ml_engine.skill_extractor import extract_skills_from_text
from ml_engine.matcher import match_candidate_to_job

router = APIRouter()

@router.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    content = await file.read()
    raw_text = extract_text_from_pdf(content)
    sections = extract_sections(raw_text)
    skills = extract_skills_from_text(raw_text)
    
    extracted_email = extract_email(raw_text)
    extracted_phone = extract_phone(raw_text)
    extracted_experience = extract_total_experience(raw_text, sections)
    
    # We could extract experience via Regex or NLP but for simplicity we'll set it to 0 or extract basic
    candidate = Candidate(
        name=file.filename.replace(".pdf", ""),
        email=extracted_email if extracted_email else f"{file.filename.split('.')[0]}@example.com",
        phone=extracted_phone,
        raw_text=raw_text,
        skills=skills,
        experience_years=extracted_experience,
        education=sections.get("education", "")
    )
    
    db.add(candidate)
    await db.commit()
    await db.refresh(candidate)
    
    # Index in ES
    await index_candidate(candidate.id, {
        "id": candidate.id,
        "name": candidate.name,
        "email": candidate.email,
        "phone": candidate.phone,
        "skills": candidate.skills,
        "experience_years": candidate.experience_years,
        "education": candidate.education,
        "clean_text": sections.get("summary", "") + " " + sections.get("experience", "")
    })
    
    return {"message": "Resume uploaded and indexed", "candidate_id": candidate.id, "skills_extracted": skills}

@router.post("/upload_jd/")
async def upload_job_description(title: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    content = await file.read()
    raw_text = content.decode("utf-8") # Assume TXT or simple text for now, or could use pdf
    
    jd_features = extract_jd_features(raw_text)
    
    job = JobDescription(
        title=title,
        description=raw_text,
        required_skills=jd_features["required_skills"],
        experience_level=jd_features["experience_years"]
    )
    
    db.add(job)
    await db.commit()
    await db.refresh(job)
    
    return {"message": "Job Description uploaded", "job_id": job.id, "required_skills": job.required_skills}

@router.get("/search/")
async def search_for_candidates(query: str, min_exp: float = 0.0):
    filters = {"min_experience": min_exp} if min_exp > 0 else None
    results = await search_candidates(query, filters)
    return {"results": results}

@router.get("/match/{candidate_id}/{job_id}")
async def match_candidate(candidate_id: int, job_id: int, db: AsyncSession = Depends(get_db)):
    # Fetch Candidate
    candidate = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = candidate.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    # Fetch Job
    job = await db.execute(select(JobDescription).where(JobDescription.id == job_id))
    job = job.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    cand_data = {
        "skills": candidate.skills,
        "experience_years": candidate.experience_years,
        "clean_text": candidate.raw_text
    }
    
    job_data = {
        "required_skills": job.required_skills,
        "experience_years": job.experience_level,
        "clean_text": job.description
    }
    
    match_results = match_candidate_to_job(cand_data, job_data)
    
    return {
        "candidate": candidate.name,
        "job": job.title,
        "match": match_results
    }
