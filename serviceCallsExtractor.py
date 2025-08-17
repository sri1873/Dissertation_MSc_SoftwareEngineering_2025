import json
import re
from collections import defaultdict

# Raw data as multiline string (representing the table from the user)
raw_data = """
S1	ts-admin-basic-info-service	4 -> S14	4->S34	4->S36	4->S11	4->S27
S2	ts-admin-order-service	4->S22	4->S23
S3	ts-admin-route-service	3-S30	1-S34
S4	ts-admin-travel-service	4-S37	4-S39	1-S34	1-S36	1-S30
S5	ts-admin-user-service	4-S40
S6	ts-assurance-service	0
S7	ts-auth-service	1-S41
S8	ts-basic-service	3-S34	2-S36	2-S30	2-S27
S9	ts-cancel-service	2-S22	2-S23	1-S40	1-S20	1-S21
S10	ts-common	0
S11	ts-config-service	0
S12	ts-consign-price-service	0
S13	ts-consign-service	2-S12
S14	ts-contacts-service	0
S15	ts-delivery-service	0
S16	ts-execute-service	2-S22	2-S23
S17	ts-food-delivery-service	1-S33
S18	ts-food-service	1-S33	1-S39	1-S35
S19	ts-gateway-service	0
S20	ts-inside-payment-service	2-S24	2-S23	2-S22
S21	ts-notification-service	0
S22	ts-order-other-service	1-S24
S23	ts-order-service	1-S24
S24	ts-payment-service	0
S25	ts-preserve-other-service	1-S8	1-S31	1-S40	1-S6	1-S34	1-S32	1-S39	1-S14	1-S13	1-S18	1-S23
S26	ts-preserve-service	1-S8	1-S31	1-S40	1-S6	1-S34	1-S32	1-S39	1-S14	1-S13	1-S18	1-S23
S27	ts-price-service	0
S28	ts-rebook-service	1-S31	4-S23	4-S22	1-S37	1-S39	1-S36	1-S30	2-S20
S29	ts-route-plan-service	2-S29	2-S39	2-S37
S30	ts-route-service	0
S31	ts-seat-service	2-S23	2-S22	1-S11
S32	ts-security-service	1-S22	1-S23
S33	ts-station-food-service	0
S34	ts-station-service	0
S35	ts-train-food-service	0
S36	ts-train-service	0
S37	ts-travel2-service	2-S8	1-S36	1-S30	1-S31
S38	ts-travel-plan-service	3-S29	1-S36	1S39	1-S37	1-S31
S39	ts-travel-service	2-S8	1-S36	1-S30	1-S31
S40	ts-user-service	2-S7
S41	ts-verification-code-service	0
S42	ts-wait-order-service	1-S14
"""

# Step 1: Map IDs to service names
service_map = {}
call_data = defaultdict(int)

lines = raw_data.strip().split('\n')
services=[]
for line in lines:
    parts = line.strip().split()
    service_id = parts[0]
    service_name = parts[1]
    service_map[service_id] = service_name
    services.append({"nanoentities":[],"id":service_id,"name":"Service "+service_id[1:]})
    for call in parts[2:]:
        match = re.match(r"(\d+)[->-]S(\d+)", call)
        if match:
            count = int(match.group(1))
            callee_id = "S" + match.group(2)
            call_data[(service_id, callee_id)] += count

# Step 2: Generate serviceCalls JSON structure
service_calls = []
for (caller_id, callee_id), count in call_data.items():
    caller_name = service_map.get(caller_id, caller_id)
    callee_name = service_map.get(callee_id, callee_id)
    service_calls.append({
        "caller": caller_name,
        "callee": callee_name,
        "callCount": count
    })
name ="train-ticket_ideal"
print(json.dumps({"name":name,"services":services,"serviceCalls": service_calls}, indent=4))
