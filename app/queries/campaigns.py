from flask import current_app
from psycopg2.extras import RealDictCursor


def get_campaings_pagination(page:int=1, size:int=10):
    offset = (page - 1) * size
    conn = current_app.db
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT
        CAMPAIGNS.ID,
        CAMPAIGNS.NAME,
        CAMPAIGNS.SUBJECT,
        COUNT(DISTINCT RECIPIENTS_MAPPING.RECIPIENT_ID) AS "total_victims",
        COUNT(EMAILS.ID) AS "total_emails",
        COUNT(DISTINCT ATTACHMENT_MAPPING.ATTACHMENT_ID) AS "total_attachments",
        MAX(EMAILS.SEND_AT) AS "timestamp"
    FROM
        CAMPAIGNS
        JOIN EMAILS ON EMAILS.CAMPAIGN_ID = CAMPAIGNS.ID
        JOIN RECIPIENTS_MAPPING ON RECIPIENTS_MAPPING.EMAIL_ID = EMAILS.ID
        JOIN ATTACHMENT_MAPPING ON ATTACHMENT_MAPPING.EMAIL_ID = EMAILS.ID
    GROUP BY
        CAMPAIGNS.ID
    ORDER BY total_emails DESC
    LIMIT %s
    OFFSET %s
    """

    count_query = "select count(*) from CAMPAIGNS"
    cursor.execute(count_query)
    total_records = cursor.fetchone()


    cursor.execute(query, (size, offset,))
    return cursor.fetchall(), total_records["count"]