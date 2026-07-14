import uuid
import requests
from playwright.sync_api import expect
BASE_URL = "https://app.workflowpro.com"
def test_project_creation_flow(page):
   project_name = f"Automation-{uuid.uuid4()}"
    token = get_auth_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": "company1"
    }
    payload = {
        "name": project_name,
        "description": "Automation Test Project",
        "team_members": [101, 102]
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/projects",
        headers=headers,
        json=payload
    )
  assert response.status_code == 201
    project_id = response.json()["id"]
    page.goto("https://company1.workflowpro.com/dashboard")
    page.wait_for_load_state("networkidle")

    expect(
        page.locator(f"text={project_name}")
    ).to_be_visible()
    logout()
    login_as_company2()
    expect(
        page.locator(f"text={project_name}")
    ).not_to_be_visible()
    requests.delete(
        f"{BASE_URL}/api/v1/projects/{project_id}",
        headers=headers
    )
