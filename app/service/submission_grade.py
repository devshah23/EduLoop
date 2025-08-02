import os
from fastapi import Depends
from huggingface_hub import InferenceClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal, get_db
from app.models.submission_model import Submission

HF_TOKEN=os.getenv('HF_TOKEN')


client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)

async def grade_sumbmission(correct_answer: list, student_answer: list,submission_id:int):
    per_question_result=[]
    async with AsyncSessionLocal() as db:
        try:
            for i in range(len(correct_answer)):    
                result = client.sentence_similarity(
                sentence=correct_answer[i],
                other_sentences=[
                student_answer[i]
                ],
                model="sentence-transformers/all-MiniLM-L12-v2",)
                per_question_result.append(result[0]*100)
            avg=sum(per_question_result)/len(per_question_result)
            print(f"Grading result: {avg}")
            
            # validate avg
            if avg < 0 or avg > 100:
                print(f'Something went wrong with grading submission-{submission_id}')
            
            result=await db.execute(select(Submission).where(Submission.id == submission_id))
            submission = result.scalar_one_or_none()
            if not submission:
                print(f"submission with ID {submission_id} not found while grading.")
                return -1
            submission.grade=avg
            await db.commit()
            await db.refresh(submission)
        except Exception as e:
            print(f"Error while grading submission: {e}")
            return -1  

