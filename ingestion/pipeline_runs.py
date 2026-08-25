def start_pipeline_run(cursor, source: str) -> int:
    """
    Create a new pipeline run record with the given
    source and return the generated pipeline run ID.
    """

    sql = """
    INSERT INTO pipeline_runs (
    source
    )
    VALUES (%s)
    RETURNING pipeline_run_id
    """

    cursor.execute(sql, (source, ))

    row = cursor.fetchone()

    return row[0]


def complete_pipeline_run(cursor, pipeline_run_id: int, records_extracted: int, records_loaded: int) -> None:
    """
    Mark an existing pipeline run as completed and record
    its completion timestamp and record counts.
    """

    sql="""
    UPDATE pipeline_runs
    SET
    status = 'completed',
    completed_at = CURRENT_TIMESTAMP,
    records_extracted = %s,
    records_loaded = %s
    WHERE pipeline_run_id = %s
    """

    cursor.execute(
        sql,
        (
            records_extracted,
            records_loaded,
            pipeline_run_id
        )
    )


def fail_pipeline_run(cursor, pipeline_run_id: int, error_message: str) -> None:
    """
    Mark an existing pipeline run as failed and record
    its completion timestamp and error message.
    """

    sql="""
    UPDATE pipeline_runs
    SET
    status = 'failed',
    completed_at = CURRENT_TIMESTAMP,
    error_message = %s
    WHERE pipeline_run_id = %s
    """

    cursor.execute(
        sql,
        (
            error_message,
            pipeline_run_id
        )
    )
