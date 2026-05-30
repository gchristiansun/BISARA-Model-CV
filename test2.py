import requests
import json
import os

BASE_URL = "https://www.kaggle.com/api/i/datasets.databundles.DatabundleService/GetDatabundleExternalChildren"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://www.kaggle.com",
    "referer": "https://www.kaggle.com/code/mpwolke/bisindo-indonesian-sign-language-mp4/input",
    "user-agent": "Mozilla/5.0",
    "x-xsrf-token": "CfDJ8G82xNY93phHtA6xMwIf8xPmv86z6uFWVXNmWgOdUn-GLg7H3I-J1nMXbGYNb2Ks5CQlasm88PpxHb4HmXXorpqm2HLp9DaTEdi5NQqz-Pl5frX3C_pQdCZHWpoa8cfpEd37I9nVz2tJpfvr6vaVCFk",
    "x-kaggle-build-version": "bc9c9ad5f824a1896ece52cf1d66ebb79049ad8a",
    "cookie": "_ga=GA1.1.1193823438.1777529795; GCLB=COTh45WytY7NtQEQAw; build-hash=bc9c9ad5f824a1896ece52cf1d66ebb79049ad8a; __Host-KAGGLEID=CfDJ8G82xNY93phHtA6xMwIf8xOu2_j40wBgc_UMSGCs9Ynb6XllkiQJ4sphnjF7zQH4eF8-3MIOpNwrcghsXQHKMZPEzpw9GeDN90WtVaIUabvAsxwYSM0AcvCO; ka_sessionid=e444e9ba283e1cb74cb9f96a3b601c44; CSRF-TOKEN=CfDJ8G82xNY93phHtA6xMwIf8xMh-D0RZXW0_n_XR1yFlcOIkd_b6h6DIqRSdybUFCc-4mX9ZXmiSUkEQ8VcHzOUTryXClPYzsrB8qrsbbyaGg; searchToken=361e9932-4655-4667-84da-3cf86beebce6; ka_db=CfDJ8G82xNY93phHtA6xMwIf8xPZ6TCIhJEAoKjE4WWD-teBsvHtdox3YrXxdFqLQDBgv2iAEeyJ9P1D8r5t-RY0Aa4Yij_57UZNYn2tA-qIYrAzc-0GnIml3t_nUyA; XSRF-TOKEN=CfDJ8G82xNY93phHtA6xMwIf8xPmv86z6uFWVXNmWgOdUn-GLg7H3I-J1nMXbGYNb2Ks5CQlasm88PpxHb4HmXXorpqm2HLp9DaTEdi5NQqz-Pl5frX3C_pQdCZHWpoa8cfpEd37I9nVz2tJpfvr6vaVCFk; CLIENT-TOKEN=eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJpc3MiOiJrYWdnbGUiLCJhdWQiOiJjbGllbnQiLCJzdWIiOiJjaHJpc3RpYW5zdW5hIiwibmJ0IjoiMjAyNi0wNS0zMFQyMDo1OTo0Ny45ODUzNzgyWiIsImlhdCI6IjIwMjYtMDUtMzBUMjA6NTk6NDcuOTg1Mzc4MloiLCJqdGkiOiI5MDM0NjQ1ZS0wNjg1LTQ5MWMtOGUyZi1lNDc5ZWY5MjA2NjkiLCJleHAiOiIyMDI2LTA2LTMwVDIwOjU5OjQ3Ljk4NTM3ODJaIiwidWlkIjoyNjU5NzQ5NiwiZGlzcGxheU5hbWUiOiJHcmVnb3JpdXMgQ2hyaXN0aWFuIFN1bmFyeW8iLCJlbWFpbCI6ImNocmlzdGlhbjEwcmtzQGdtYWlsLmNvbSIsInRpZXIiOiJjb250cmlidXRvciIsInZlcmlmaWVkIjp0cnVlLCJwcm9maWxlVXJsIjoiL2NocmlzdGlhbnN1bmEiLCJ0aHVtYm5haWxVcmwiOiJodHRwczovL3N0b3JhZ2UuZ29vZ2xlYXBpcy5jb20va2FnZ2xlLWF2YXRhcnMvdGh1bWJuYWlscy8yNjU5NzQ5Ni1rZy5wbmc_dD0yMDI2LTAyLTE3LTEyLTE1LTUzIiwiZmZoIjoiNzA4MDg2MmI5ZDBmMzI0Y2QwNmFmYzEyZWZhODQyNGY3MTQ1ZGFiMWEwYzhkOGY2NTFiMzU2MjFiNTcyMThmZSIsInBpZCI6ImthZ2dsZS0xNjE2MDciLCJzdmMiOiJ3ZWItZmUiLCJzZGFrIjoiQUl6YVN5QTRlTnFVZFJSc2tKc0NaV1Z6LXFMNjU1WGE1SkVNcmVFIiwiYmxkIjoiYmM5YzlhZDVmODI0YTE4OTZlY2U1MmNmMWQ2NmViYjc5MDQ5YWQ4YSJ9.; _ga_T7QHS60L4Q=GS2.1.s1780174785$o16$g1$t1780174787$j58$l0$h0"
}

verification_info = {
    "datasetId": 1175079,
    "databundleVersionId": 2006713
}

all_files = []

def scrape_directory(path):

    payload = {
        "verificationInfo": verification_info,
        "count": 100,
        "depth": 1,
        "firestorePath": path,
        "offset": 0,
    }

    r = requests.post(
        BASE_URL,
        json=payload,
        headers=headers
    )

    print("STATUS:", r.status_code)

    data = r.json()

    # DIRECTORIES
    for d in data.get("directories", []):

        print("DIR:", d["name"])

        scrape_directory(d["path"])

    # FILES
    for f in data.get("files", []):

        print("FILE:", f["name"])

        all_files.append(f)

root_path = "urgCSGmHGQVYP0I147DK/versions/dVdLOkY5lIYDAuN0Fi3C/directories/bisindo - video dataset"

scrape_directory(root_path)

print("\nTOTAL FILES:", len(all_files))

with open("files.json", "w", encoding="utf-8") as fp:
    json.dump(all_files, fp, indent=2)