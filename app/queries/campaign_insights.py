from flask import current_app
from psycopg2.extras import RealDictCursor


def get_campaign_insights(campaign_id:int, page:int=1, size:int=10, ):
    offset = (page - 1) * size
    stats_query = """SELECT
        COUNT(DISTINCT RECIPIENTS_MAPPING.RECIPIENT_ID) AS "total_victims",
        COUNT(EMAILS.ID) AS "total_emails",
        COUNT(DISTINCT ATTACHMENT_MAPPING.ATTACHMENT_ID) AS "total_attachments",
        COUNT(DISTINCT EMAILS.sender_id) as "total_sender_count"
    FROM
        CAMPAIGNS
        JOIN EMAILS ON EMAILS.CAMPAIGN_ID = CAMPAIGNS.ID
        JOIN RECIPIENTS_MAPPING ON RECIPIENTS_MAPPING.EMAIL_ID = EMAILS.ID
        JOIN ATTACHMENT_MAPPING ON ATTACHMENT_MAPPING.EMAIL_ID = EMAILS.ID
    WHERE CAMPAIGNS.ID = %s
    GROUP BY
        CAMPAIGNS.ID
    ORDER BY total_emails DESC"""

    conn = current_app.db
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute(stats_query, (campaign_id,))

    stats_result = cursor.fetchone()

    main_query = """WITH
        RECIPIENTS_DETAIL AS (
            SELECT
                EMAIL_ID,
                COUNT(*) AS RECIPIENT_COUNT
            FROM
                RECIPIENTS_MAPPING
            GROUP BY
                EMAIL_ID
        ),
        ATTACHMENT_DETAIL AS (
            SELECT
                EMAIL_ID,
                COUNT(*) AS ATTACHMENT_COUNT
            FROM
                ATTACHMENT_MAPPING
                JOIN ATTACHMENTS ON ATTACHMENTS.ID = ATTACHMENT_MAPPING.ATTACHMENT_ID
            GROUP BY
                EMAIL_ID
        )
    SELECT
        EMAILS.ID,
        CAMPAIGNS.SUBJECT,
        SENDERS.EMAIL,
        EMAILS.SENDER_IP,
        RECIPIENTS_DETAIL.RECIPIENT_COUNT,
        COALESCE(ATTACHMENT_DETAIL.ATTACHMENT_COUNT, 0) AS TOTAL_ATTACHMENTS,
        EMAILS.SEND_AT
    FROM
        EMAILS
        JOIN SENDERS ON SENDERS.ID = EMAILS.SENDER_ID
        JOIN RECIPIENTS_DETAIL ON RECIPIENTS_DETAIL.EMAIL_ID = EMAILS.ID
        LEFT JOIN ATTACHMENT_DETAIL ON ATTACHMENT_DETAIL.EMAIL_ID = EMAILS.ID
        JOIN CAMPAIGNS ON CAMPAIGNS.ID = EMAILS.CAMPAIGN_ID
    WHERE
        EMAILS.CAMPAIGN_ID = %s
    ORDER BY EMAILS.ID DESC
        LIMIT %s
    OFFSET %s"""
    
    cursor.execute(main_query, (campaign_id,size, offset))

    records = cursor.fetchall()

    count_query = "select count(*) from EMAILS WHERE CAMPAIGN_ID = %s"
    cursor.execute(count_query, (campaign_id,))
    total_records = cursor.fetchone()


    return stats_result, records, total_records["count"]