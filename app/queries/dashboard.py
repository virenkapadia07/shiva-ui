from flask import current_app

def get_sender_count():
    conn = current_app.db

    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM senders;')  
    count = cursor.fetchone()[0]
    return count


def get_receiver_count():
    conn = current_app.db

    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM recipients;')  
    count = cursor.fetchone()[0]
    return count

def get_processed_email_count():
    conn = current_app.db

    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM emails;')  
    count = cursor.fetchone()[0]
    return count

def get_email_campaigns_count():
    conn = current_app.db

    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM campaigns;')  
    count = cursor.fetchone()[0]
    return count

def get_attachment_count():
    conn = current_app.db

    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM attachments;')  
    count = cursor.fetchone()[0]
    return count

def get_ips_count():
    conn = current_app.db

    cursor = conn.cursor()
    cursor.execute('select count(DISTINCT emails.sender_ip) from emails')  
    count = cursor.fetchone()[0]
    return count

def get_email_processed_per_day():
    conn = current_app.db

    cursor = conn.cursor()
    query = """SELECT
        DATE(send_at) AS day,
        COUNT(*) AS count
    FROM
        emails
    GROUP BY
        DATE(send_at)
    ORDER BY
        day;"""
    cursor.execute(query)  
    records = cursor.fetchall()
    result = {
        "labels" : [],
        "data" :[]
    }
    for record in records:
        result["labels"].append(str(record[0]))
        result["data"].append(record[1])

    return result

def get_top_file_extensions():
    conn = current_app.db

    cursor = conn.cursor()
    query = """select file_extension, count(*) from attachments
    GROUP BY file_extension
    ORDER BY count(*) LIMIT 10"""
    cursor.execute(query)  
    records = cursor.fetchall()
    result = {
        "labels" : [],
        "data" :[]
    }
    for record in records:
        result["labels"].append(str(record[0]))
        result["data"].append(record[1])

    return result

def get_top_campaigns():
    conn = current_app.db

    cursor = conn.cursor()
    query = """SELECT
	CAMPAIGNS.NAME,
	COUNT(*)
    FROM
        PUBLIC.EMAILS
        JOIN PUBLIC.CAMPAIGNS ON CAMPAIGNS.ID = EMAILS.CAMPAIGN_ID
    GROUP BY
        CAMPAIGN_ID,
        CAMPAIGNS.NAME
    ORDER BY
        COUNT(*) DESC LIMIT 20;"""
    cursor.execute(query)  
    records = cursor.fetchall()
    result = []
    for record in records:
        result.append({
            "x" : str(record[0]),
            "y" : record[1]
        })

    return result


def get_top_user_agents():
    conn = current_app.db

    cursor = conn.cursor()
    query = """SELECT
	USER_AGENT,
        COUNT(*)
    FROM
        PUBLIC.EMAILS
    WHERE
        USER_AGENT IS NOT NULL
    GROUP BY
        USER_AGENT
    ORDER BY
        COUNT(*) DESC LIMIT 10;"""
    cursor.execute(query)  
    records = cursor.fetchall()
    result = {
        "labels" : [],
        "data" :[]
    }
    for record in records:
        result["labels"].append(str(record[0]))
        result["data"].append(record[1])

    return result


def get_top_url_domains():
    conn = current_app.db

    cursor = conn.cursor()
    query = """SELECT
        domain,
        COUNT(*)
    FROM
        urls
    GROUP BY
        domain
    ORDER BY
        COUNT(*) DESC LIMIT 10;"""
    cursor.execute(query)  
    records = cursor.fetchall()
    result = {
        "labels" : [],
        "data" :[]
    }
    for record in records:
        result["labels"].append(str(record[0]))
        result["data"].append(record[1])

    return result

def get_top_sender_ips():

    conn = current_app.db

    cursor = conn.cursor()
    query = """SELECT
	SENDER_IP,
	COUNT(*)
    FROM
        EMAILS
    GROUP BY
        SENDER_IP
    ORDER BY
        COUNT(*) DESC
        LIMIT 10"""
    
    cursor.execute(query)  
    records = cursor.fetchall()
    result = {
        "labels" : [],
        "data" :[]
    }
    for record in records:
        result["labels"].append(str(record[0]))
        result["data"].append(record[1])

    return result


def get_top_targeted_domains():
    conn = current_app.db

    cursor = conn.cursor()
    query = """SELECT
        RECIPIENTS."domain",
        COUNT(*)
    FROM
        EMAILS
        JOIN RECIPIENTS_MAPPING ON RECIPIENTS_MAPPING.EMAIL_ID = EMAILS.ID
        JOIN RECIPIENTS ON RECIPIENTS.ID = RECIPIENTS_MAPPING.RECIPIENT_ID
    GROUP BY
        RECIPIENTS."domain"
    ORDER BY
        COUNT(*) DESC
    LIMIT
        10"""
    
    cursor.execute(query)  
    records = cursor.fetchall()
    result = {
        "labels" : [],
        "data" :[]
    }
    for record in records:
        result["labels"].append(str(record[0]))
        result["data"].append(record[1])

    return result