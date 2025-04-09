from fastapi import APIRouter
from sqlmodel import text

from app.engine.database_session import SessionDep

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/quarter-by-quarter/", status_code=200)
async def retrieve_quarter_by_quarter_analysis(session: SessionDep):

    result = session.exec(text(
        """
        SELECT 
            d.department,
            j.job,
            SUM(CASE WHEN SUBSTR(e.datetime, 6, 2) IN ('01', '02', '03') THEN 1 ELSE 0 END) AS q1,
            SUM(CASE WHEN SUBSTR(e.datetime, 6, 2) IN ('04', '05', '06') THEN 1 ELSE 0 END) AS q2,
            SUM(CASE WHEN SUBSTR(e.datetime, 6, 2) IN ('07', '08', '09') THEN 1 ELSE 0 END) AS q3,
            SUM(CASE WHEN SUBSTR(e.datetime, 6, 2) IN ('10', '11', '12') THEN 1 ELSE 0 END) AS q4
        FROM employee e
        LEFT JOIN department d
            ON e.department_id = d.id
        LEFT JOIN job j
            ON e.job_id = j.id
        WHERE SUBSTR(e.datetime, 1, 4) = '2021'
        GROUP BY d.department, j.job
        ORDER BY d.department ASC, j.job ASC        
        """
    ))
    records = result.all()

    columns = ["department", "job", "Q1", "Q2", "Q3", "Q4"]
    records_data = [dict(zip(columns, row)) for row in records]

    return records_data


@router.get("/top-hiring-departments/", status_code=200)
async def retrive_top_hiring_departments(session: SessionDep) -> list[dict]:

    result = session.exec(text(
        """
        SELECT
            d.department,
            COUNT(*) AS hired
        FROM employee e
        LEFT JOIN department d
            ON e.department_id = d.id
        WHERE substr(e.datetime, 1, 4) = '2021'
        GROUP BY d.department
        HAVING COUNT(*) > (
            SELECT AVG(dept_hires) FROM (
                SELECT COUNT(*) AS dept_hires
                FROM employee
                WHERE substr(datetime, 1, 4) = '2021'
                GROUP BY department_id
            )
        )
        ORDER BY hired DESC;
        """
    ))
    records = result.all()

    columns = ["department", "hired"]
    records_data = [dict(zip(columns, row)) for row in records]

    return records_data
