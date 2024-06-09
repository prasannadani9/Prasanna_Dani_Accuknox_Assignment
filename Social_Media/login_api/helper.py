import re

def check_for_error_login_api(data):
    error_map = {
        "email": "Email Id Not Provided",
        "password": "Password Not Provided"
    }
    for mandatory_field in error_map.keys():
        if mandatory_field not in data:
            return False, error_map.get(mandatory_field)
    
    email_regex = r"(^([a-zA-Z0-9_\-\.]+)@([a-zA-Z\-]+)\.(com|in|co.in|net|org|info|edu|mil|gov|biz|aero|museum|name|coop|arpa|pro)$)"
    email = data.get("email", "").strip().lower() 

    if not re.match(email_regex, email):
        return False, "Invalid Email Format"
    
    else: 
        return True, " "

def check_for_error_signup_api(data):
    err_map = {
        "email": "Email Id Not Provided",
        "name": "Name Not Provided",
        "password": "Password Not Provided"
    }
    for key, val in err_map.items():
        if key not in data or not data.get(key, "") or not data.get(key, "").strip():
            return False, val
    
    email_regex = r"(^([a-zA-Z0-9_\-\.]+)@([a-zA-Z\-]+)\.(com|in|co.in|net|org|info|edu|mil|gov|biz|aero|museum|name|coop|arpa|pro)$)"
    email = data.get("email", "").strip().lower() 

    if not re.match(email_regex, email):
        return False, "Invalid Email Format"
    
    else: 
        return True, " "