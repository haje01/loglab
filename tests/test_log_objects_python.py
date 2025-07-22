#!/usr/bin/env python3
"""
Basic tests for Python log objects generated from foo.lab.json
"""
import json
import os
import tempfile
from datetime import datetime

from loglab_foo import *


def test_basic_log_objects():
    """Test basic functionality of generated log objects"""

    # Test Login event
    login = Login(1, 10000, "ios")
    login.AcntId = 12345
    login.ServerNo = 1
    login.Platform = "ios"

    # Test serialization
    login_json = login.serialize()
    login_data = json.loads(login_json)

    assert login_data["AcntId"] == 12345
    assert login_data["ServerNo"] == 1
    assert login_data["Platform"] == "ios"
    assert "DateTime" in login_data
    assert login_data["Category"] == 1

    # Test Logout event
    logout = Logout(1, 10000)
    logout.AcntId = 12345
    logout.ServerNo = 1
    logout.PlayTime = 3600.5

    logout_json = logout.serialize()
    logout_data = json.loads(logout_json)

    assert logout_data["AcntId"] == 12345
    assert logout_data["PlayTime"] == 3600.5

    # Test KillMonster event
    kill_monster = KillMonster(1, 1234, 5678, 1001, 100.5, 200.7, 0.0, 5001, 999888)
    kill_json = kill_monster.serialize()
    kill_data = json.loads(kill_json)

    assert kill_data["CharId"] == 5678
    assert kill_data["MonsterCd"] == 5001
    assert kill_data["PosX"] == 100.5

    # Test reset functionality
    login.reset(2, 20000, "aos")
    login_reset_json = login.serialize()
    login_reset_data = json.loads(login_reset_json)

    assert login_reset_data["AcntId"] == 20000
    assert login_reset_data["ServerNo"] == 2
    assert login_reset_data["Platform"] == "aos"
