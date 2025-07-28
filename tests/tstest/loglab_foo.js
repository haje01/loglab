"use strict";
/*

    ** 이 파일은 LogLab 에서 생성된 것입니다. 고치지 마세요! **

    Domain: foo
    Description: 위대한 모바일 게임

*/
Object.defineProperty(exports, "__esModule", { value: true });
exports.GetItem = exports.MonsterDropItem = exports.KillMonster = exports.CharLogout = exports.CharLogin = exports.Logout = exports.Login = void 0;
/**
 * 계정 로그인
 */
var Login = /** @class */ (function () {
    function Login(_ServerNo, _AcntId, _Platform) {
        this.Event = "Login";
        this.reset(_ServerNo, _AcntId, _Platform);
    }
    Login.prototype.reset = function (_ServerNo, _AcntId, _Platform) {
        this.ServerNo = _ServerNo;
        this.AcntId = _AcntId;
        this.Platform = _Platform;
    };
    Login.prototype.serialize = function () {
        var data = {
            DateTime: new Date().toISOString(),
            Event: "Login"
        };
        data["ServerNo"] = this.ServerNo;
        data["AcntId"] = this.AcntId;
        data["Category"] = 1;
        data["Platform"] = this.Platform;
        return JSON.stringify(data);
    };
    return Login;
}());
exports.Login = Login;
/**
 * 계정 로그아웃
 */
var Logout = /** @class */ (function () {
    function Logout(_ServerNo, _AcntId) {
        this.Event = "Logout";
        // 플레이 시간 (초)
        this.PlayTime = null;
        this.reset(_ServerNo, _AcntId);
    }
    Logout.prototype.reset = function (_ServerNo, _AcntId) {
        this.ServerNo = _ServerNo;
        this.AcntId = _AcntId;
        this.PlayTime = null;
    };
    Logout.prototype.serialize = function () {
        var data = {
            DateTime: new Date().toISOString(),
            Event: "Logout"
        };
        data["ServerNo"] = this.ServerNo;
        data["AcntId"] = this.AcntId;
        data["Category"] = 1;
        if (this.PlayTime !== null) {
            data["PlayTime"] = this.PlayTime;
        }
        return JSON.stringify(data);
    };
    return Logout;
}());
exports.Logout = Logout;
/**
 * 캐릭터 로그인
 */
var CharLogin = /** @class */ (function () {
    function CharLogin(_ServerNo, _AcntId, _CharId) {
        this.Event = "CharLogin";
        this.reset(_ServerNo, _AcntId, _CharId);
    }
    CharLogin.prototype.reset = function (_ServerNo, _AcntId, _CharId) {
        this.ServerNo = _ServerNo;
        this.AcntId = _AcntId;
        this.CharId = _CharId;
    };
    CharLogin.prototype.serialize = function () {
        var data = {
            DateTime: new Date().toISOString(),
            Event: "CharLogin"
        };
        data["ServerNo"] = this.ServerNo;
        data["AcntId"] = this.AcntId;
        data["Category"] = 2;
        data["CharId"] = this.CharId;
        return JSON.stringify(data);
    };
    return CharLogin;
}());
exports.CharLogin = CharLogin;
/**
 * 캐릭터 로그아웃
 */
var CharLogout = /** @class */ (function () {
    function CharLogout(_ServerNo, _AcntId, _CharId) {
        this.Event = "CharLogout";
        this.reset(_ServerNo, _AcntId, _CharId);
    }
    CharLogout.prototype.reset = function (_ServerNo, _AcntId, _CharId) {
        this.ServerNo = _ServerNo;
        this.AcntId = _AcntId;
        this.CharId = _CharId;
    };
    CharLogout.prototype.serialize = function () {
        var data = {
            DateTime: new Date().toISOString(),
            Event: "CharLogout"
        };
        data["ServerNo"] = this.ServerNo;
        data["AcntId"] = this.AcntId;
        data["Category"] = 2;
        data["CharId"] = this.CharId;
        return JSON.stringify(data);
    };
    return CharLogout;
}());
exports.CharLogout = CharLogout;
/**
 * 몬스터를 잡음
 */
var KillMonster = /** @class */ (function () {
    function KillMonster(_ServerNo, _AcntId, _CharId, _MapCd, _PosX, _PosY, _PosZ, _MonsterCd, _MonsterId) {
        this.Event = "KillMonster";
        this.reset(_ServerNo, _AcntId, _CharId, _MapCd, _PosX, _PosY, _PosZ, _MonsterCd, _MonsterId);
    }
    KillMonster.prototype.reset = function (_ServerNo, _AcntId, _CharId, _MapCd, _PosX, _PosY, _PosZ, _MonsterCd, _MonsterId) {
        this.ServerNo = _ServerNo;
        this.AcntId = _AcntId;
        this.CharId = _CharId;
        this.MapCd = _MapCd;
        this.PosX = _PosX;
        this.PosY = _PosY;
        this.PosZ = _PosZ;
        this.MonsterCd = _MonsterCd;
        this.MonsterId = _MonsterId;
    };
    KillMonster.prototype.serialize = function () {
        var data = {
            DateTime: new Date().toISOString(),
            Event: "KillMonster"
        };
        data["ServerNo"] = this.ServerNo;
        data["AcntId"] = this.AcntId;
        data["Category"] = 2;
        data["CharId"] = this.CharId;
        data["MapCd"] = this.MapCd;
        data["PosX"] = this.PosX;
        data["PosY"] = this.PosY;
        data["PosZ"] = this.PosZ;
        data["MonsterCd"] = this.MonsterCd;
        data["MonsterId"] = this.MonsterId;
        return JSON.stringify(data);
    };
    return KillMonster;
}());
exports.KillMonster = KillMonster;
/**
 * 몬스터가 아이템을 떨어뜨림
 */
var MonsterDropItem = /** @class */ (function () {
    function MonsterDropItem(_ServerNo, _MonsterCd, _MonsterId, _MapCd, _PosX, _PosY, _PosZ, _ItemCd, _ItemId) {
        this.Event = "MonsterDropItem";
        this.reset(_ServerNo, _MonsterCd, _MonsterId, _MapCd, _PosX, _PosY, _PosZ, _ItemCd, _ItemId);
    }
    MonsterDropItem.prototype.reset = function (_ServerNo, _MonsterCd, _MonsterId, _MapCd, _PosX, _PosY, _PosZ, _ItemCd, _ItemId) {
        this.ServerNo = _ServerNo;
        this.MonsterCd = _MonsterCd;
        this.MonsterId = _MonsterId;
        this.MapCd = _MapCd;
        this.PosX = _PosX;
        this.PosY = _PosY;
        this.PosZ = _PosZ;
        this.ItemCd = _ItemCd;
        this.ItemId = _ItemId;
    };
    MonsterDropItem.prototype.serialize = function () {
        var data = {
            DateTime: new Date().toISOString(),
            Event: "MonsterDropItem"
        };
        data["ServerNo"] = this.ServerNo;
        data["Category"] = 3;
        data["MonsterCd"] = this.MonsterCd;
        data["MonsterId"] = this.MonsterId;
        data["MapCd"] = this.MapCd;
        data["PosX"] = this.PosX;
        data["PosY"] = this.PosY;
        data["PosZ"] = this.PosZ;
        data["ItemCd"] = this.ItemCd;
        data["ItemId"] = this.ItemId;
        return JSON.stringify(data);
    };
    return MonsterDropItem;
}());
exports.MonsterDropItem = MonsterDropItem;
/**
 * 캐릭터의 아이템 습득
 */
var GetItem = /** @class */ (function () {
    function GetItem(_ServerNo, _AcntId, _CharId, _MapCd, _PosX, _PosY, _PosZ, _ItemCd, _ItemId) {
        this.Event = "GetItem";
        this.reset(_ServerNo, _AcntId, _CharId, _MapCd, _PosX, _PosY, _PosZ, _ItemCd, _ItemId);
    }
    GetItem.prototype.reset = function (_ServerNo, _AcntId, _CharId, _MapCd, _PosX, _PosY, _PosZ, _ItemCd, _ItemId) {
        this.ServerNo = _ServerNo;
        this.AcntId = _AcntId;
        this.CharId = _CharId;
        this.MapCd = _MapCd;
        this.PosX = _PosX;
        this.PosY = _PosY;
        this.PosZ = _PosZ;
        this.ItemCd = _ItemCd;
        this.ItemId = _ItemId;
    };
    GetItem.prototype.serialize = function () {
        var data = {
            DateTime: new Date().toISOString(),
            Event: "GetItem"
        };
        data["ServerNo"] = this.ServerNo;
        data["AcntId"] = this.AcntId;
        data["Category"] = 2;
        data["CharId"] = this.CharId;
        data["MapCd"] = this.MapCd;
        data["PosX"] = this.PosX;
        data["PosY"] = this.PosY;
        data["PosZ"] = this.PosZ;
        data["ItemCd"] = this.ItemCd;
        data["ItemId"] = this.ItemId;
        return JSON.stringify(data);
    };
    return GetItem;
}());
exports.GetItem = GetItem;
