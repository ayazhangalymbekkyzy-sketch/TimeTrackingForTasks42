"""
FastAPI: Учёт времени на задачи (мини-журнал)
- POST /ingest  — добавить одну или несколько записей
- GET  /summary — сводка: total_minutes + таблица задача → сумма минут
- GET  /export  — скачать tasks_summary.csv
- GET  /chart   — PNG горизонтальный bar-график топ-5 задач

# документация по API: http://127.0.0.1:8000/docs
"""

from __future__ import annotations

import io
from typing import Optional

import matplotlib
matplotlib.use("Agg")

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

from TaskManager import TaskManager          # Неделя 9  — валидация
from TimeTracker import TimeTracker          # Неделя 10 — numpy
from TimeJournal import TimeJournal          # Неделя 11 — DataFrame
from TimeJournalSummary import TimeJournalSummary  # Неделя 12 — groupby + CSV
from TimeJournalChart import TimeJournalChart      # Неделя 13 — matplotlib


app = FastAPI(title="Week 14: Time Tracker")

task_manager     = TaskManager()          # нед. 9
time_tracker     = TimeTracker()          # нед. 10
time_journal     = TimeJournal()          # нед. 11
journal_summary  = TimeJournalSummary()   # нед. 12
journal_chart    = TimeJournalChart()     # нед. 13


class TaskRecord(BaseModel):
    task_name: str = Field(min_length=1, max_length=200)
    minutes: int = Field(gt=0)
    date: str  # YYYY-MM-DD

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("date должно быть в формате YYYY-MM-DD")
        return v


class IngestPayload(BaseModel):
    records: list[TaskRecord] = Field(min_length=1)


class TaskSummaryRow(BaseModel):
    task_name: str
    total_minutes: int


class SummaryResponse(BaseModel):
    total_minutes: int
    by_task: list[TaskSummaryRow]


def _add_to_all(task_name: str, minutes: int, date: str) -> None:
    """Добавляет запись во все классы одновременно."""
    task_manager.add_task(task_name, minutes, date)   # нед. 9
    time_tracker.add_record(task_name, minutes, date) # нед. 10
    time_journal.add_record(task_name, minutes, date) # нед. 11
    journal_summary.add_record(task_name, minutes, date)  # нед. 12
    journal_chart.add_record(task_name, minutes, date)    # нед. 13



@app.post("/ingest", status_code=201)
def ingest(payload: IngestPayload) -> dict:
    """
    Принять одну или несколько записей и добавить в журнал.

    Пример тела запроса:
    {
      "records": [
        {"task_name": "Coding", "minutes": 90, "date": "2025-01-15"},
        {"task_name": "Review", "minutes": 30, "date": "2025-01-15"}
      ]
    }
    """
    for rec in payload.records:
        _add_to_all(rec.task_name, rec.minutes, rec.date)

    return {
        "added": len(payload.records),
        "total_records": len(journal_summary.records),
    }


@app.get("/summary", response_model=SummaryResponse)
def summary(
    top: Optional[int] = Query(default=None, ge=1, description="Показать только топ-N задач"),
) -> SummaryResponse:
    """
    Вернуть total_minutes (numpy, нед.10) и сводку задача → сумма минут (pandas groupby, нед.12).
    """
    if not journal_summary.records:
        raise HTTPException(status_code=404, detail="Записей пока нет")

    # total_minutes — через numpy (неделя 10)
    total = time_tracker.total_minutes()

    # сводка по задачам — через pandas groupby (неделя 12)
    summary_df = journal_summary.get_summary()

    if top is not None:
        summary_df = summary_df.head(top)

    rows = [
        TaskSummaryRow(
            task_name=row["task_name"],
            total_minutes=int(row["minutes"]),
        )
        for _, row in summary_df.iterrows()
    ]

    return SummaryResponse(total_minutes=int(total), by_task=rows)


@app.get("/export")
def export_csv() -> StreamingResponse:
    """
    Скачать tasks_summary.csv (неделя 12 — save_to_csv).
    """
    if not journal_summary.records:
        raise HTTPException(status_code=404, detail="Записей пока нет")

    tmp_path = "tasks_summary.csv"
    journal_summary.save_to_csv(tmp_path)  # нед. 12

    with open(tmp_path, "r", encoding="utf-8") as f:
        content = f.read()

    return StreamingResponse(
        iter([content]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tasks_summary.csv"},
    )


@app.get("/chart")
def get_chart() -> Response:
    """
    Горизонтальный bar-график топ-5 задач → PNG (неделя 13 — plot_top5).
    """
    if not journal_chart.records:
        raise HTTPException(status_code=404, detail="Записей пока нет")

    tmp_path = "top5_tasks.png"
    journal_chart.plot_top5(filename=tmp_path)  # нед. 13

    with open(tmp_path, "rb") as f:
        img_bytes = f.read()

    return Response(content=img_bytes, media_type="image/png")