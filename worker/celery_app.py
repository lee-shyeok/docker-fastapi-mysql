from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def process_item(item_id: int, name: str):
    print(f"Processing item {item_id}: {name}")
    return {"status": "done", "item_id": item_id}