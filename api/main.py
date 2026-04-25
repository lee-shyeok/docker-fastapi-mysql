from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models
from .database import engine, get_db, Base
from .llm import get_llm_response
from pydantic import BaseModel

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class MessageRequest(BaseModel):
    content: str

@app.post("/conversations")
async def create_conversation(db: AsyncSession = Depends(get_db)):
    conv = models.Conversation()
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return conv

@app.post("/conversations/{conv_id}/messages")
async def send_message(conv_id: int, req: MessageRequest, db: AsyncSession = Depends(get_db)):
    user_msg = models.Message(conversation_id=conv_id, role="user", content=req.content)
    db.add(user_msg)
    await db.commit()

    result = await db.execute(select(models.Message).where(models.Message.conversation_id == conv_id))
    history = result.scalars().all()
    messages = [{"role": m.role, "content": m.content} for m in history]

    reply = await get_llm_response(messages)

    ai_msg = models.Message(conversation_id=conv_id, role="assistant", content=reply)
    db.add(ai_msg)
    await db.commit()
    await db.refresh(ai_msg)
    return ai_msg

@app.get("/conversations/{conv_id}/messages")
async def get_messages(conv_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Message).where(models.Message.conversation_id == conv_id))
    return result.scalars().all()