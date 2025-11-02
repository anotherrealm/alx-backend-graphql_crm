#!/bin/bash
#deletes customers in the last one year with 0 orders

LOG_FILE="/tmp/customer_cleanup_log.txt"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

#activate django environ
cd /path/to/your/project 
source venv/bin/activate  # virtualenv

#django command
DELETED=$(python manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta
cutoff = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(last_order__lt=cutoff).delete()
print(deleted)
")

count=$(python manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta
cutoff = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(last_order__lt=cutoff).delete()
print(deleted)
")

#log the result
echo \"[$TIMESTAMP] Deleted $count inactive customers.\" >> $LOG_FILE
