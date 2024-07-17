from flask import Flask, jsonify
from sqlalchemy import create_engine
import pandas as pd
import sqlite3

app = Flask(__name__)
DATABASE_URI = 'sqlite:///test.db'
engine = create_engine(DATABASE_URI)

# Endpoint para la primera consulta
@app.route('/employees_per_job_and_department', methods=['GET'])
def employees_per_job_and_department():
    query = """
    SELECT 
        d.department AS department, 
        j.job AS job,
        SUM(CASE WHEN strftime('%m', e.hire_date) IN ('01', '02', '03') THEN 1 ELSE 0 END) AS Q1,
        SUM(CASE WHEN strftime('%m', e.hire_date) IN ('04', '05', '06') THEN 1 ELSE 0 END) AS Q2,
        SUM(CASE WHEN strftime('%m', e.hire_date) IN ('07', '08', '09') THEN 1 ELSE 0 END) AS Q3,
        SUM(CASE WHEN strftime('%m', e.hire_date) IN ('10', '11', '12') THEN 1 ELSE 0 END) AS Q4
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    JOIN jobs j ON e.job_id = j.id
    WHERE strftime('%Y', e.hire_date) = '2021'
    GROUP BY department, job
    ORDER BY department, job;
    """
    conn = sqlite3.connect('test.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return jsonify(df.to_dict(orient='records'))

# Endpoint para la segunda consulta
@app.route('/departments_above_average_hires', methods=['GET'])
def departments_above_average_hires():
    query = """
    WITH dept_hires AS (
        SELECT 
            d.id, 
            d.department, 
            COUNT(e.id) AS hired
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        WHERE strftime('%Y', e.hire_date) = '2021'
        GROUP BY d.id, d.department
    ),
    average_hires AS (
        SELECT AVG(hired) AS avg_hired FROM dept_hires
    )
    SELECT 
        dh.id, 
        dh.department, 
        dh.hired
    FROM dept_hires dh, average_hires ah
    WHERE dh.hired > ah.avg_hired
    ORDER BY dh.hired DESC;
    """
    conn = sqlite3.connect('test.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
