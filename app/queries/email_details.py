from flask import current_app
from psycopg2.extras import RealDictCursor


def get_email_details(email_id:int):
    query = """WITH
        RECIPIENTS_DETAIL AS (
            SELECT
                EMAIL_ID,
                ARRAY_AGG(DISTINCT RECIPIENTS.EMAIL) AS UNIQUE_RECIPIENTS
            FROM
                RECIPIENTS_MAPPING
                JOIN RECIPIENTS ON RECIPIENTS.ID = RECIPIENTS_MAPPING.RECIPIENT_ID
            GROUP BY
                EMAIL_ID
        ),
        ATTACHMENT_DETAIL AS (
            SELECT
                EMAIL_ID,
                COALESCE(
                    (
                        SELECT
                            JSONB_AGG(ATTACHMENTS)
                    ),
                    '[]'::JSONB
                ) AS ATTACHMENTS_DETAILS
            FROM
                ATTACHMENT_MAPPING
                JOIN ATTACHMENTS ON ATTACHMENTS.ID = ATTACHMENT_MAPPING.ATTACHMENT_ID
            GROUP BY
                EMAIL_ID
        ),
        URL_DETAIL AS (
            SELECT
                EMAIL_ID,
                COALESCE(
                    (
                        SELECT
                            JSONB_AGG(URLS)
                    ),
                    '[]'::JSONB
                ) AS URLS_DETAILS
            FROM
                URL_MAPPING
                JOIN URLS ON URLS.ID = URL_MAPPING.URL_ID
            GROUP BY
                EMAIL_ID
        )
    SELECT
        EMAILS.ID,
        CAMPAIGNS.SUBJECT,
        SENDERS.EMAIL,
        EMAILS.SENDER_IP,
        RECIPIENTS_DETAIL.UNIQUE_RECIPIENTS,
        ATTACHMENT_DETAIL.ATTACHMENTS_DETAILS,
        URL_DETAIL.URLS_DETAILS,
        EMAILS.SEND_AT,
        CAMPAIGNS.EMAIL_BODY
    FROM
        EMAILS
        JOIN SENDERS ON SENDERS.ID = EMAILS.SENDER_ID
        JOIN RECIPIENTS_DETAIL ON RECIPIENTS_DETAIL.EMAIL_ID = EMAILS.ID
        LEFT JOIN ATTACHMENT_DETAIL ON ATTACHMENT_DETAIL.EMAIL_ID = EMAILS.ID
        LEFT JOIN URL_DETAIL ON URL_DETAIL.EMAIL_ID = EMAILS.ID
        JOIN CAMPAIGNS ON CAMPAIGNS.ID = EMAILS.CAMPAIGN_ID
    WHERE
        EMAILS.ID = %s
    """

    conn = current_app.db
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute(query, (email_id,))

    result = cursor.fetchone()

    return result