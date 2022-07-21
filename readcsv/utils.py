import csv
from .models import File
import io
from datetime import  datetime


def save_uploaded_file(request):
    try:
        file = request.FILES['file']
        # file = file.read()
        file = file.read().decode()
        io_string = io.StringIO(file)
        csvreader = csv.reader(io_string)
        next(csvreader)
        to_create = []
        for row in csvreader:
            item_dict = {
                "transaction_id": row[0],
                "transaction_time": datetime.strptime(row[1], "%Y%m%d %H%M%S"),
                "product_name": row[2],
                "quantity": row[3],
                "unit_price": row[4],
                "total_price": row[5],
                "delivered_to_city": row[6]
            }
            to_create.append(File(**item_dict))
        if to_create:
            File.objects.bulk_create(to_create)
            return True, "File saved successfully"
        return False, "Oops file could not be saved"
    except Exception as e:
        return False, e

