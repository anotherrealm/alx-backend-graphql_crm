#!/usr/bin/env python3
"""
Queries GraphQL API for pending orders in the last 7 days, logs them
"""

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

#configure
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/order_reminders_log.txt"

def main():
    #get the date
    today = datetime.now()
    one_week_ago = today - timedelta(days=7)

    #graqhql query
    query = gql("""
    query GetRecentPendingOrders($startDate: DateTime!) {
      orders(orderDate_Gte: $startDate, status: "PENDING") {
        id
        customer {
          email
        }
      }
    }
    """)

    #start the graphql client
    transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT, verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    #execute query
    try:
        result = client.execute(query, variable_values={"startDate": one_week_ago.isoformat()})
        orders = result.get("orders", [])
    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{today}] ERROR: Failed to fetch orders - {e}\n")
        return

    #log each order
    with open(LOG_FILE, "a") as f:
        f.write(f"\n[{today.strftime('%Y-%m-%d %H:%M:%S')}] Processing {len(orders)} pending orders:\n")
        for order in orders:
            order_id = order.get("id")
            email = order.get("customer", {}).get("email", "N/A")
            f.write(f"Order ID: {order_id}, Customer Email: {email}\n")

    print("Order reminders processed!")

if __name__ == "__main__":
    main()
