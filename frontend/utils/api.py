import requests
import streamlit as st
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api").rstrip("/")
REQUEST_TIMEOUT = (5, 120)

def get_headers():
    headers = {"Content-Type": "application/json"}
    if "token" in st.session_state and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    return headers

def handle_response(response):
    if response.status_code >= 200 and response.status_code < 300:
        try:
            return response.json()
        except ValueError:
            return response.text
    else:
        try:
            error = response.json()
            error_msg = error.get("detail", str(error))
        except ValueError:
            error_msg = response.text
        st.error(f"API Error: {error_msg}")
        return None

def request(method, endpoint, **kwargs):
    headers = get_headers()
    if kwargs.get("files"):
        headers.pop("Content-Type", None) # Let requests set the multipart boundary
    try:
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            headers=headers,
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )
    except requests.RequestException as exc:
        st.error(f"Could not reach the API: {exc}")
        return None
    return handle_response(response)

def post(endpoint, data=None, files=None):
    if files:
        return request("POST", endpoint, data=data, files=files)
    return request("POST", endpoint, json=data)

def get(endpoint, params=None):
    return request("GET", endpoint, params=params)

def delete(endpoint):
    return request("DELETE", endpoint)

def put(endpoint, data=None):
    return request("PUT", endpoint, json=data)
