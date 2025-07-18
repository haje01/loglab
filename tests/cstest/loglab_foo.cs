/*

    ** 이 파일은 LogLab 에서 생성된 것입니다. 고치지 마세요! **

    Domain: foo
    Description: 위대한 모바일 게임

*/

using System;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Text.Encodings.Web;
using System.Text.Unicode;
using System.Collections.Generic;
using System.Diagnostics;

namespace loglab_foo
{
    /// <summary>
    ///  계정 로그인
    /// </summary>
    public class Login
    {
        public const string Event = "Login";
        // 서버 번호
        public int? ServerNo = null;
        // 계정 ID
        public int? AcntId = null;
        // 이벤트 분류
        public int? Category = null;
        // 디바이스의 플랫폼
        public string? Platform = null;
        public static JsonSerializerOptions options = new JsonSerializerOptions
        {
            Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        };

        public Login(int _ServerNo, int _AcntId, string _Platform)
        {
            Reset(_ServerNo, _AcntId, _Platform);
        }
        public void Reset(int _ServerNo, int _AcntId, string _Platform)
        {
            ServerNo = _ServerNo;
            AcntId = _AcntId;
            Platform = _Platform;
        }
        public string Serialize()
        {
            List<string> fields = new List<string>();
            Debug.Assert(ServerNo.HasValue);
            fields.Add($"\"ServerNo\": {ServerNo}");
            Debug.Assert(AcntId.HasValue);
            fields.Add($"\"AcntId\": {AcntId}");
            fields.Add($"\"Category\": 1");
            Debug.Assert(Platform != null);
            Platform = JsonSerializer.Serialize(Platform, Login.options);
            fields.Add($"\"Platform\": {Platform}");
            string sfields = String.Join(", ", fields);
            string dt = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss.fffzzz");
            string sjson = $"{{\"DateTime\": \"{dt}\", \"Event\": \"{Event}\", {sfields}}}";
            return sjson;
        }
    }
    /// <summary>
    ///  계정 로그아웃
    /// </summary>
    public class Logout
    {
        public const string Event = "Logout";
        // 서버 번호
        public int? ServerNo = null;
        // 계정 ID
        public int? AcntId = null;
        // 이벤트 분류
        public int? Category = null;
        // 플레이 시간 (초)
        public float? PlayTime = null;
        public static JsonSerializerOptions options = new JsonSerializerOptions
        {
            Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        };

        public Logout(int _ServerNo, int _AcntId)
        {
            Reset(_ServerNo, _AcntId);
        }
        public void Reset(int _ServerNo, int _AcntId)
        {
            ServerNo = _ServerNo;
            AcntId = _AcntId;
            PlayTime = null;
        }
        public string Serialize()
        {
            List<string> fields = new List<string>();
            Debug.Assert(ServerNo.HasValue);
            fields.Add($"\"ServerNo\": {ServerNo}");
            Debug.Assert(AcntId.HasValue);
            fields.Add($"\"AcntId\": {AcntId}");
            fields.Add($"\"Category\": 1");
            if (PlayTime.HasValue)
                fields.Add($"\"PlayTime\": {PlayTime}");
            string sfields = String.Join(", ", fields);
            string dt = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss.fffzzz");
            string sjson = $"{{\"DateTime\": \"{dt}\", \"Event\": \"{Event}\", {sfields}}}";
            return sjson;
        }
    }
    /// <summary>
    ///  캐릭터 로그인
    /// </summary>
    public class CharLogin
    {
        public const string Event = "CharLogin";
        // 서버 번호
        public int? ServerNo = null;
        // 계정 ID
        public int? AcntId = null;
        // 이벤트 분류
        public int? Category = null;
        // 캐릭터 ID
        public int? CharId = null;
        public static JsonSerializerOptions options = new JsonSerializerOptions
        {
            Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        };

        public CharLogin(int _ServerNo, int _AcntId, int _CharId)
        {
            Reset(_ServerNo, _AcntId, _CharId);
        }
        public void Reset(int _ServerNo, int _AcntId, int _CharId)
        {
            ServerNo = _ServerNo;
            AcntId = _AcntId;
            CharId = _CharId;
        }
        public string Serialize()
        {
            List<string> fields = new List<string>();
            Debug.Assert(ServerNo.HasValue);
            fields.Add($"\"ServerNo\": {ServerNo}");
            Debug.Assert(AcntId.HasValue);
            fields.Add($"\"AcntId\": {AcntId}");
            fields.Add($"\"Category\": 2");
            Debug.Assert(CharId.HasValue);
            fields.Add($"\"CharId\": {CharId}");
            string sfields = String.Join(", ", fields);
            string dt = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss.fffzzz");
            string sjson = $"{{\"DateTime\": \"{dt}\", \"Event\": \"{Event}\", {sfields}}}";
            return sjson;
        }
    }
    /// <summary>
    ///  캐릭터 로그아웃
    /// </summary>
    public class CharLogout
    {
        public const string Event = "CharLogout";
        // 서버 번호
        public int? ServerNo = null;
        // 계정 ID
        public int? AcntId = null;
        // 이벤트 분류
        public int? Category = null;
        // 캐릭터 ID
        public int? CharId = null;
        public static JsonSerializerOptions options = new JsonSerializerOptions
        {
            Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        };

        public CharLogout(int _ServerNo, int _AcntId, int _CharId)
        {
            Reset(_ServerNo, _AcntId, _CharId);
        }
        public void Reset(int _ServerNo, int _AcntId, int _CharId)
        {
            ServerNo = _ServerNo;
            AcntId = _AcntId;
            CharId = _CharId;
        }
        public string Serialize()
        {
            List<string> fields = new List<string>();
            Debug.Assert(ServerNo.HasValue);
            fields.Add($"\"ServerNo\": {ServerNo}");
            Debug.Assert(AcntId.HasValue);
            fields.Add($"\"AcntId\": {AcntId}");
            fields.Add($"\"Category\": 2");
            Debug.Assert(CharId.HasValue);
            fields.Add($"\"CharId\": {CharId}");
            string sfields = String.Join(", ", fields);
            string dt = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss.fffzzz");
            string sjson = $"{{\"DateTime\": \"{dt}\", \"Event\": \"{Event}\", {sfields}}}";
            return sjson;
        }
    }
    /// <summary>
    ///  몬스터를 잡음
    /// </summary>
    public class KillMonster
    {
        public const string Event = "KillMonster";
        // 서버 번호
        public int? ServerNo = null;
        // 계정 ID
        public int? AcntId = null;
        // 이벤트 분류
        public int? Category = null;
        // 캐릭터 ID
        public int? CharId = null;
        // 맵 코드
        public int? MapCd = null;
        // 맵상 X 위치
        public float? PosX = null;
        // 맵상 Y 위치
        public float? PosY = null;
        // 맵상 Z 위치
        public float? PosZ = null;
        // 몬스터 타입 코드
        public int? MonsterCd = null;
        // 몬스터 개체 ID
        public int? MonsterId = null;
        public static JsonSerializerOptions options = new JsonSerializerOptions
        {
            Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        };

        public KillMonster(int _ServerNo, int _AcntId, int _CharId, int _MapCd, float _PosX, float _PosY, float _PosZ, int _MonsterCd, int _MonsterId)
        {
            Reset(_ServerNo, _AcntId, _CharId, _MapCd, _PosX, _PosY, _PosZ, _MonsterCd, _MonsterId);
        }
        public void Reset(int _ServerNo, int _AcntId, int _CharId, int _MapCd, float _PosX, float _PosY, float _PosZ, int _MonsterCd, int _MonsterId)
        {
            ServerNo = _ServerNo;
            AcntId = _AcntId;
            CharId = _CharId;
            MapCd = _MapCd;
            PosX = _PosX;
            PosY = _PosY;
            PosZ = _PosZ;
            MonsterCd = _MonsterCd;
            MonsterId = _MonsterId;
        }
        public string Serialize()
        {
            List<string> fields = new List<string>();
            Debug.Assert(ServerNo.HasValue);
            fields.Add($"\"ServerNo\": {ServerNo}");
            Debug.Assert(AcntId.HasValue);
            fields.Add($"\"AcntId\": {AcntId}");
            fields.Add($"\"Category\": 2");
            Debug.Assert(CharId.HasValue);
            fields.Add($"\"CharId\": {CharId}");
            Debug.Assert(MapCd.HasValue);
            fields.Add($"\"MapCd\": {MapCd}");
            Debug.Assert(PosX.HasValue);
            fields.Add($"\"PosX\": {PosX}");
            Debug.Assert(PosY.HasValue);
            fields.Add($"\"PosY\": {PosY}");
            Debug.Assert(PosZ.HasValue);
            fields.Add($"\"PosZ\": {PosZ}");
            Debug.Assert(MonsterCd.HasValue);
            fields.Add($"\"MonsterCd\": {MonsterCd}");
            Debug.Assert(MonsterId.HasValue);
            fields.Add($"\"MonsterId\": {MonsterId}");
            string sfields = String.Join(", ", fields);
            string dt = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss.fffzzz");
            string sjson = $"{{\"DateTime\": \"{dt}\", \"Event\": \"{Event}\", {sfields}}}";
            return sjson;
        }
    }
    /// <summary>
    ///  몬스터가 아이템을 떨어뜨림
    /// </summary>
    public class MonsterDropItem
    {
        public const string Event = "MonsterDropItem";
        // 서버 번호
        public int? ServerNo = null;
        // 이벤트 분류
        public int? Category = null;
        // 몬스터 타입 코드
        public int? MonsterCd = null;
        // 몬스터 개체 ID
        public int? MonsterId = null;
        // 맵 코드
        public int? MapCd = null;
        // 맵상 X 위치
        public float? PosX = null;
        // 맵상 Y 위치
        public float? PosY = null;
        // 맵상 Z 위치
        public float? PosZ = null;
        // 아이템 타입 코드
        public int? ItemCd = null;
        // 아이템 개체 ID
        public int? ItemId = null;
        public static JsonSerializerOptions options = new JsonSerializerOptions
        {
            Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        };

        public MonsterDropItem(int _ServerNo, int _MonsterCd, int _MonsterId, int _MapCd, float _PosX, float _PosY, float _PosZ, int _ItemCd, int _ItemId)
        {
            Reset(_ServerNo, _MonsterCd, _MonsterId, _MapCd, _PosX, _PosY, _PosZ, _ItemCd, _ItemId);
        }
        public void Reset(int _ServerNo, int _MonsterCd, int _MonsterId, int _MapCd, float _PosX, float _PosY, float _PosZ, int _ItemCd, int _ItemId)
        {
            ServerNo = _ServerNo;
            MonsterCd = _MonsterCd;
            MonsterId = _MonsterId;
            MapCd = _MapCd;
            PosX = _PosX;
            PosY = _PosY;
            PosZ = _PosZ;
            ItemCd = _ItemCd;
            ItemId = _ItemId;
        }
        public string Serialize()
        {
            List<string> fields = new List<string>();
            Debug.Assert(ServerNo.HasValue);
            fields.Add($"\"ServerNo\": {ServerNo}");
            fields.Add($"\"Category\": 3");
            Debug.Assert(MonsterCd.HasValue);
            fields.Add($"\"MonsterCd\": {MonsterCd}");
            Debug.Assert(MonsterId.HasValue);
            fields.Add($"\"MonsterId\": {MonsterId}");
            Debug.Assert(MapCd.HasValue);
            fields.Add($"\"MapCd\": {MapCd}");
            Debug.Assert(PosX.HasValue);
            fields.Add($"\"PosX\": {PosX}");
            Debug.Assert(PosY.HasValue);
            fields.Add($"\"PosY\": {PosY}");
            Debug.Assert(PosZ.HasValue);
            fields.Add($"\"PosZ\": {PosZ}");
            Debug.Assert(ItemCd.HasValue);
            fields.Add($"\"ItemCd\": {ItemCd}");
            Debug.Assert(ItemId.HasValue);
            fields.Add($"\"ItemId\": {ItemId}");
            string sfields = String.Join(", ", fields);
            string dt = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss.fffzzz");
            string sjson = $"{{\"DateTime\": \"{dt}\", \"Event\": \"{Event}\", {sfields}}}";
            return sjson;
        }
    }
    /// <summary>
    ///  캐릭터의 아이템 습득
    /// </summary>
    public class GetItem
    {
        public const string Event = "GetItem";
        // 서버 번호
        public int? ServerNo = null;
        // 계정 ID
        public int? AcntId = null;
        // 이벤트 분류
        public int? Category = null;
        // 캐릭터 ID
        public int? CharId = null;
        // 맵 코드
        public int? MapCd = null;
        // 맵상 X 위치
        public float? PosX = null;
        // 맵상 Y 위치
        public float? PosY = null;
        // 맵상 Z 위치
        public float? PosZ = null;
        // 아이템 타입 코드
        public int? ItemCd = null;
        // 아이템 개체 ID
        public int? ItemId = null;
        public static JsonSerializerOptions options = new JsonSerializerOptions
        {
            Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        };

        public GetItem(int _ServerNo, int _AcntId, int _CharId, int _MapCd, float _PosX, float _PosY, float _PosZ, int _ItemCd, int _ItemId)
        {
            Reset(_ServerNo, _AcntId, _CharId, _MapCd, _PosX, _PosY, _PosZ, _ItemCd, _ItemId);
        }
        public void Reset(int _ServerNo, int _AcntId, int _CharId, int _MapCd, float _PosX, float _PosY, float _PosZ, int _ItemCd, int _ItemId)
        {
            ServerNo = _ServerNo;
            AcntId = _AcntId;
            CharId = _CharId;
            MapCd = _MapCd;
            PosX = _PosX;
            PosY = _PosY;
            PosZ = _PosZ;
            ItemCd = _ItemCd;
            ItemId = _ItemId;
        }
        public string Serialize()
        {
            List<string> fields = new List<string>();
            Debug.Assert(ServerNo.HasValue);
            fields.Add($"\"ServerNo\": {ServerNo}");
            Debug.Assert(AcntId.HasValue);
            fields.Add($"\"AcntId\": {AcntId}");
            fields.Add($"\"Category\": 2");
            Debug.Assert(CharId.HasValue);
            fields.Add($"\"CharId\": {CharId}");
            Debug.Assert(MapCd.HasValue);
            fields.Add($"\"MapCd\": {MapCd}");
            Debug.Assert(PosX.HasValue);
            fields.Add($"\"PosX\": {PosX}");
            Debug.Assert(PosY.HasValue);
            fields.Add($"\"PosY\": {PosY}");
            Debug.Assert(PosZ.HasValue);
            fields.Add($"\"PosZ\": {PosZ}");
            Debug.Assert(ItemCd.HasValue);
            fields.Add($"\"ItemCd\": {ItemCd}");
            Debug.Assert(ItemId.HasValue);
            fields.Add($"\"ItemId\": {ItemId}");
            string sfields = String.Join(", ", fields);
            string dt = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss.fffzzz");
            string sjson = $"{{\"DateTime\": \"{dt}\", \"Event\": \"{Event}\", {sfields}}}";
            return sjson;
        }
    }
}