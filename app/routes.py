from flask import Blueprint, render_template, request

from app.queries.campaign_insights import get_campaign_insights
from app.queries.campaigns import get_campaings_pagination
from app.queries.dashboard import get_attachment_count, get_email_campaigns_count, get_email_processed_per_day, get_ips_count, get_processed_email_count, get_receiver_count, get_sender_count, get_top_campaigns, get_top_file_extensions, get_top_sender_ips, get_top_targeted_domains, get_top_url_domains
from app.queries.email_details import get_email_details

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    all_data = {}
    # Stats
    all_data["sender_count"] = get_sender_count()
    all_data["receiver_count"] = get_receiver_count()
    all_data["processed_email_count"] = get_processed_email_count()
    all_data["email_campaigns_count"] = get_email_campaigns_count()
    all_data["attachment_count"] = get_attachment_count()
    all_data["ips_count"] = get_ips_count()

    # Graphs
    all_data["per_day_email"]  = get_email_processed_per_day()
    all_data["top_file_exensions"] = get_top_file_extensions()
    all_data["top_campaigns"] = get_top_campaigns()
    all_data["top_url_domains"] = get_top_url_domains()
    all_data["top_sender_ips"] = get_top_sender_ips()
    all_data["top_targeted_domains"] = get_top_targeted_domains()


    return render_template('index.html', records=all_data)

@main.route('/campaigns')
def campaigns():
    page = request.args.get("page", 1, int)
    size = request.args.get("page", 10, int)
    results, total_records = get_campaings_pagination()
    total_pages = (total_records + size - 1) // size
    return render_template('campaigns.html', records=results, page=page, size=size, total_pages=total_pages)


@main.route('/campaigns/<int:id>')
def campaign_insights(id):
    page = request.args.get("page", 1, int)
    size = request.args.get("size", 10, int)
    stats, records, total_records = get_campaign_insights(id, page, size)
    total_pages = (total_records + size - 1) // size

    page_range = list(range(max(1, page - 2), min(total_pages + 1, page + 3)))
    return render_template('campaign_insights.html', stats = stats,  records=records, page=page, size=size, total_pages=total_pages, page_range=page_range, campaign_id=id)

@main.route('/campaigns/<int:campaign_id>/mails/<int:mail_id>')
def email_details(campaign_id, mail_id):
    record = get_email_details(mail_id)
    print(record)
    return render_template('email_details.html', record=record)