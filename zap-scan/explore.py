import re
import time
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET = "http://web:5000"
PROXY = "http://zap:8090"

SESSION = requests.Session()
SESSION.proxies = {"http": PROXY, "https": PROXY}
SESSION.verify = False

USERNAME = "zapdast"
PASSWORD = "ZapDast@123"


def get_csrf(html):
    m = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
    return m.group(1) if m else None


def get(url):
    r = SESSION.get(url)
    r.raise_for_status()
    print(f"GET  {url} -> {r.status_code}")
    return r.text


def post(url, data):
    r = SESSION.post(url, data=data)
    r.raise_for_status()
    print(f"POST {url} -> {r.status_code}")
    return r.text


def wait_for_proxy():
    for i in range(30):
        try:
            r = SESSION.get(f"{TARGET}/", timeout=5)
            print(f"Proxy ready (attempt {i + 1})")
            return
        except (requests.ConnectionError, requests.ProxyError):
            print(f"Waiting for proxy... (attempt {i + 1})")
            time.sleep(5)
    raise RuntimeError("ZAP proxy did not become ready in time")


def main():
    wait_for_proxy()

    # 1. About page
    get(f"{TARGET}/")

    # 2. Register a new user
    html = get(f"{TARGET}/register")
    csrf = get_csrf(html)
    if csrf:
        post(f"{TARGET}/register", {
            "csrf_token": csrf,
            "username": USERNAME,
            "password": PASSWORD,
            "confirm_password": PASSWORD,
            "submit": "Register",
        })

    # 3. Login
    html = get(f"{TARGET}/login")
    csrf = get_csrf(html)
    if csrf:
        post(f"{TARGET}/login", {
            "csrf_token": csrf,
            "username": USERNAME,
            "password": PASSWORD,
            "submit": "Login",
        })

    # 4. All tasks page (authenticated)
    html = get(f"{TARGET}/all_tasks")

    # 5. Add tasks
    for i in range(1, 4):
        html = get(f"{TARGET}/add_task")
        csrf = get_csrf(html)
        if csrf:
            post(f"{TARGET}/add_task", {
                "csrf_token": csrf,
                "task_name": f"ZAP test task {i}",
                "submit": "Add Task",
            })

    # 6. View all tasks again
    html = get(f"{TARGET}/all_tasks")

    # 7. Update the first task if any exist
    task_ids = re.findall(r"/all_tasks/(\d+)/update_task", html)
    if task_ids:
        tid = task_ids[0]
        html = get(f"{TARGET}/all_tasks/{tid}/update_task")
        csrf = get_csrf(html)
        if csrf:
            post(f"{TARGET}/all_tasks/{tid}/update_task", {
                "csrf_token": csrf,
                "task_name": f"Updated ZAP task {tid}",
                "submit": "Save Changes",
            })

    # 8. Account page
    html = get(f"{TARGET}/account")
    csrf = get_csrf(html)
    if csrf:
        post(f"{TARGET}/account", {
            "csrf_token": csrf,
            "username": USERNAME,
            "submit": "Update Info",
        })

    # 9. Change password page
    html = get(f"{TARGET}/account/change_password")
    csrf = get_csrf(html)
    if csrf:
        post(f"{TARGET}/account/change_password", {
            "csrf_token": csrf,
            "old_password": PASSWORD,
            "new_password": PASSWORD,
            "submit": "Change password",
        })

    # 10. Logout
    get(f"{TARGET}/logout")

    print("Exploration complete. All traffic recorded by ZAP.")


if __name__ == "__main__":
    main()
