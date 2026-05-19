from pathlib import Path


def test_deploy_workflow_targets_cardbot_service_and_keeps_env_external():
    workflow = Path(".github/workflows/deploy.yml").read_text(encoding="utf-8")

    assert "branches:\n      - main" in workflow
    assert "/opt/cardbot/" in workflow
    assert "systemctl restart cardbot" in workflow
    assert "--exclude '.env'" in workflow
    assert "--exclude '.env.example'" in workflow
    assert "EnvironmentFile" not in workflow
