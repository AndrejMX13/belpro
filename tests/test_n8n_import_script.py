"""Unit tests for n8n_workflows.py — resolve_workflow_refs logic."""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "scripts"))
from n8n_workflows import resolve_workflow_refs


def test_resolves_error_workflow_setting():
    payload = {
        "name": "BelPro - Vnos Prostovoljcev",
        "settings": {"errorWorkflow": "BelPro - Napake"},
        "nodes": [],
    }
    n8n_by_name = {"BelPro - Napake": "abc123"}
    changed = resolve_workflow_refs(payload, n8n_by_name)
    assert changed
    assert payload["settings"]["errorWorkflow"] == "abc123"


def test_resolves_node_workflow_id():
    payload = {
        "name": "BelPro - Vnos Prostovoljcev",
        "settings": {},
        "nodes": [{"parameters": {"workflowId": "BelPro - Napake"}}],
    }
    n8n_by_name = {"BelPro - Napake": "abc123"}
    changed = resolve_workflow_refs(payload, n8n_by_name)
    assert changed
    assert payload["nodes"][0]["parameters"]["workflowId"] == "abc123"


def test_no_change_when_already_id():
    payload = {
        "name": "BelPro - Vnos Prostovoljcev",
        "settings": {"errorWorkflow": "abc123"},
        "nodes": [],
    }
    n8n_by_name = {"BelPro - Napake": "abc123"}
    changed = resolve_workflow_refs(payload, n8n_by_name)
    assert not changed
    assert payload["settings"]["errorWorkflow"] == "abc123"


def test_no_change_when_setting_absent():
    payload = {"name": "test", "settings": {}, "nodes": []}
    changed = resolve_workflow_refs(payload, {"BelPro - Napake": "abc123"})
    assert not changed


def test_resolves_both_at_once():
    payload = {
        "name": "test",
        "settings": {"errorWorkflow": "BelPro - Napake"},
        "nodes": [{"parameters": {"workflowId": "BelPro - Napake"}}],
    }
    n8n_by_name = {"BelPro - Napake": "xyz999"}
    changed = resolve_workflow_refs(payload, n8n_by_name)
    assert changed
    assert payload["settings"]["errorWorkflow"] == "xyz999"
    assert payload["nodes"][0]["parameters"]["workflowId"] == "xyz999"
