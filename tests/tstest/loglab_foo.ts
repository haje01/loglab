/*

    ** 이 파일은 LogLab 에서 생성된 것입니다. 고치지 마세요! **

    Domain: foo
    Description: 위대한 모바일 게임

*/


/**
 * 계정 로그인
 */
export class Login {
    public readonly Event = "Login";
    // 서버 번호
    public ServerNo: number;
    // 계정 ID
    public AcntId: number;
    // 디바이스의 플랫폼
    public Platform: string;

    constructor(_ServerNo: number, _AcntId: number, _Platform: string) {
        this.reset(_ServerNo, _AcntId, _Platform);
    }

    public reset(_ServerNo: number, _AcntId: number, _Platform: string): void {
        this.ServerNo = _ServerNo;
        this.AcntId = _AcntId;
        this.Platform = _Platform;
    }

    public serialize(): string {
        const data: Record<string, any> = {
            DateTime: new Date().toISOString(),
            Event: "Login"
        };
        data["ServerNo"] = this.ServerNo;
        data["AcntId"] = this.AcntId;
        data["Category"] = 1;
        data["Platform"] = this.Platform;
        return JSON.stringify(data);
    }
}

/**
 * 계정 로그아웃
 */
export class Logout {
    public readonly Event = "Logout";
    // 서버 번호
    public ServerNo: number;
    // 계정 ID
    public AcntId: number;
    // 플레이 시간 (초)
    public PlayTime: number | null = null;

    constructor(_ServerNo: number, _AcntId: number) {
        this.reset(_ServerNo, _AcntId);
    }

    public reset(_ServerNo: number, _AcntId: number): void {
        this.ServerNo = _ServerNo;
        this.AcntId = _AcntId;
        this.PlayTime = null;
    }

    public serialize(): string {
        const data: Record<string, any> = {
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
    }
}

/**
 * 캐릭터 로그인
 */
export class CharLogin {
    public readonly Event = "CharLogin";
    // 서버 번호
    public ServerNo: number;
    // 계정 ID
    public AcntId: number;
    // 캐릭터 ID
    public CharId: number;

    constructor(_ServerNo: number, _AcntId: number, _CharId: number) {
        this.reset(_ServerNo, _AcntId, _CharId);
    }

    public reset(_ServerNo: number, _AcntId: number, _CharId: number): void {
        this.ServerNo = _ServerNo;
        this.AcntId = _AcntId;
        this.CharId = _CharId;
    }

    public serialize(): string {
        const data: Record<string, any> = {
            DateTime: new Date().toISOString(),
            Event: "CharLogin"
        };
        data["ServerNo"] = this.ServerNo;
        data["AcntId"] = this.AcntId;
        data["Category"] = 2;
        data["CharId"] = this.CharId;
        return JSON.stringify(data);
    }
}

/**
 * 캐릭터 로그아웃
 */
export class CharLogout {
    public readonly Event = "CharLogout";
    // 서버 번호
    public ServerNo: number;
    // 계정 ID
    public AcntId: number;
    // 캐릭터 ID
    public CharId: number;

    constructor(_ServerNo: number, _AcntId: number, _CharId: number) {
        this.reset(_ServerNo, _AcntId, _CharId);
    }

    public reset(_ServerNo: number, _AcntId: number, _CharId: number): void {
        this.ServerNo = _ServerNo;
        this.AcntId = _AcntId;
        this.CharId = _CharId;
    }

    public serialize(): string {
        const data: Record<string, any> = {
            DateTime: new Date().toISOString(),
            Event: "CharLogout"
        };
        data["ServerNo"] = this.ServerNo;
        data["AcntId"] = this.AcntId;
        data["Category"] = 2;
        data["CharId"] = this.CharId;
        return JSON.stringify(data);
    }
}

/**
 * 몬스터를 잡음
 */
export class KillMonster {
    public readonly Event = "KillMonster";
    // 서버 번호
    public ServerNo: number;
    // 계정 ID
    public AcntId: number;
    // 캐릭터 ID
    public CharId: number;
    // 맵 코드
    public MapCd: number;
    // 맵상 X 위치
    public PosX: number;
    // 맵상 Y 위치
    public PosY: number;
    // 맵상 Z 위치
    public PosZ: number;
    // 몬스터 타입 코드
    public MonsterCd: number;
    // 몬스터 개체 ID
    public MonsterId: number;

    constructor(_ServerNo: number, _AcntId: number, _CharId: number, _MapCd: number, _PosX: number, _PosY: number, _PosZ: number, _MonsterCd: number, _MonsterId: number) {
        this.reset(_ServerNo, _AcntId, _CharId, _MapCd, _PosX, _PosY, _PosZ, _MonsterCd, _MonsterId);
    }

    public reset(_ServerNo: number, _AcntId: number, _CharId: number, _MapCd: number, _PosX: number, _PosY: number, _PosZ: number, _MonsterCd: number, _MonsterId: number): void {
        this.ServerNo = _ServerNo;
        this.AcntId = _AcntId;
        this.CharId = _CharId;
        this.MapCd = _MapCd;
        this.PosX = _PosX;
        this.PosY = _PosY;
        this.PosZ = _PosZ;
        this.MonsterCd = _MonsterCd;
        this.MonsterId = _MonsterId;
    }

    public serialize(): string {
        const data: Record<string, any> = {
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
    }
}

/**
 * 몬스터가 아이템을 떨어뜨림
 */
export class MonsterDropItem {
    public readonly Event = "MonsterDropItem";
    // 서버 번호
    public ServerNo: number;
    // 몬스터 타입 코드
    public MonsterCd: number;
    // 몬스터 개체 ID
    public MonsterId: number;
    // 맵 코드
    public MapCd: number;
    // 맵상 X 위치
    public PosX: number;
    // 맵상 Y 위치
    public PosY: number;
    // 맵상 Z 위치
    public PosZ: number;
    // 아이템 타입 코드
    public ItemCd: number;
    // 아이템 개체 ID
    public ItemId: number;

    constructor(_ServerNo: number, _MonsterCd: number, _MonsterId: number, _MapCd: number, _PosX: number, _PosY: number, _PosZ: number, _ItemCd: number, _ItemId: number) {
        this.reset(_ServerNo, _MonsterCd, _MonsterId, _MapCd, _PosX, _PosY, _PosZ, _ItemCd, _ItemId);
    }

    public reset(_ServerNo: number, _MonsterCd: number, _MonsterId: number, _MapCd: number, _PosX: number, _PosY: number, _PosZ: number, _ItemCd: number, _ItemId: number): void {
        this.ServerNo = _ServerNo;
        this.MonsterCd = _MonsterCd;
        this.MonsterId = _MonsterId;
        this.MapCd = _MapCd;
        this.PosX = _PosX;
        this.PosY = _PosY;
        this.PosZ = _PosZ;
        this.ItemCd = _ItemCd;
        this.ItemId = _ItemId;
    }

    public serialize(): string {
        const data: Record<string, any> = {
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
    }
}

/**
 * 캐릭터의 아이템 습득
 */
export class GetItem {
    public readonly Event = "GetItem";
    // 서버 번호
    public ServerNo: number;
    // 계정 ID
    public AcntId: number;
    // 캐릭터 ID
    public CharId: number;
    // 맵 코드
    public MapCd: number;
    // 맵상 X 위치
    public PosX: number;
    // 맵상 Y 위치
    public PosY: number;
    // 맵상 Z 위치
    public PosZ: number;
    // 아이템 타입 코드
    public ItemCd: number;
    // 아이템 개체 ID
    public ItemId: number;

    constructor(_ServerNo: number, _AcntId: number, _CharId: number, _MapCd: number, _PosX: number, _PosY: number, _PosZ: number, _ItemCd: number, _ItemId: number) {
        this.reset(_ServerNo, _AcntId, _CharId, _MapCd, _PosX, _PosY, _PosZ, _ItemCd, _ItemId);
    }

    public reset(_ServerNo: number, _AcntId: number, _CharId: number, _MapCd: number, _PosX: number, _PosY: number, _PosZ: number, _ItemCd: number, _ItemId: number): void {
        this.ServerNo = _ServerNo;
        this.AcntId = _AcntId;
        this.CharId = _CharId;
        this.MapCd = _MapCd;
        this.PosX = _PosX;
        this.PosY = _PosY;
        this.PosZ = _PosZ;
        this.ItemCd = _ItemCd;
        this.ItemId = _ItemId;
    }

    public serialize(): string {
        const data: Record<string, any> = {
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
    }
}
