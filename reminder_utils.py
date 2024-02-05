from database_manager import DatabaseManager

def fetch_surgeries_at(target_date):
    db_manager = DatabaseManager('ameliyat_yonetim.db')
    query = "SELECT * FROM ameliyatlar WHERE tarih = ?"
    # Format target_date to match your database date format
    formatted_date = target_date.strftime("%Y-%m-%d %H:%M")
    results = db_manager.execute_query(query, (formatted_date,)).fetchall()
    # Assuming results are returned in a dict-like format or converting them to one
    surgeries = [{'email': row['email'], 'phone_number': row['phone_number']} for row in results]
    return surgeries
