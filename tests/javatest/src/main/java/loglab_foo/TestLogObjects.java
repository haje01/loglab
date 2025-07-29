package loglab_foo;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Basic tests for Java log objects generated from foo.lab.json
 */
public class TestLogObjects {
    private static final ObjectMapper mapper = new ObjectMapper();

    public static void main(String[] args) {
        System.out.println("Testing Java Log Objects...");

        try {
            // Test basic object creation and serialization
            testBasicFunctionality();

            System.out.println("✓ All Java log object tests passed!");
        } catch (Exception ex) {
            System.err.println("✗ Test failed: " + ex.getMessage());
            ex.printStackTrace();
            System.exit(1);
        }
    }

    private static void testBasicFunctionality() throws Exception {
        System.out.println("Testing basic log object functionality...");

        // Test Login event
        Login login = new Login(1, 12345, "ios");
        String loginJson = login.serialize();
        System.out.println("Login JSON: " + loginJson);

        // Validate JSON structure
        JsonNode loginNode = mapper.readTree(loginJson);
        validateBasicStructure(loginNode, "Login");
        assert loginNode.get("ServerNo").asInt() == 1;
        assert loginNode.get("AcntId").asInt() == 12345;
        assert loginNode.get("Platform").asText().equals("ios");
        assert loginNode.get("Category").asInt() == 1;
        System.out.println("✓ Login event serialization test passed");

        // Test Logout event
        Logout logout = new Logout(1, 12345);
        String logoutJson = logout.serialize();
        System.out.println("Logout JSON: " + logoutJson);

        JsonNode logoutNode = mapper.readTree(logoutJson);
        validateBasicStructure(logoutNode, "Logout");
        assert logoutNode.get("ServerNo").asInt() == 1;
        assert logoutNode.get("AcntId").asInt() == 12345;
        assert logoutNode.get("Category").asInt() == 1;
        // PlayTime should not be present since it's not set
        assert !logoutNode.has("PlayTime");
        System.out.println("✓ Logout event serialization test passed");

        // Test Logout with optional field
        logout.setPlayTime(123.45f);
        String logoutWithPlayTimeJson = logout.serialize();
        System.out.println("Logout with PlayTime JSON: " + logoutWithPlayTimeJson);

        JsonNode logoutWithPlayTimeNode = mapper.readTree(logoutWithPlayTimeJson);
        assert logoutWithPlayTimeNode.has("PlayTime");
        assert Math.abs(logoutWithPlayTimeNode.get("PlayTime").asDouble() - 123.45) < 0.001;
        System.out.println("✓ Optional field test passed");

        // Test KillMonster event
        KillMonster killMonster = new KillMonster(1, 12345, 67890, 1001, 100.5f, 200.7f, 0.0f, 5001, 999888);
        String killMonsterJson = killMonster.serialize();
        System.out.println("KillMonster JSON: " + killMonsterJson);

        JsonNode killMonsterNode = mapper.readTree(killMonsterJson);
        validateBasicStructure(killMonsterNode, "KillMonster");
        assert killMonsterNode.get("ServerNo").asInt() == 1;
        assert killMonsterNode.get("AcntId").asInt() == 12345;
        assert killMonsterNode.get("CharId").asInt() == 67890;
        assert killMonsterNode.get("MapCd").asInt() == 1001;
        assert Math.abs(killMonsterNode.get("PosX").asDouble() - 100.5) < 0.001;
        assert Math.abs(killMonsterNode.get("PosY").asDouble() - 200.7) < 0.001;
        assert Math.abs(killMonsterNode.get("PosZ").asDouble() - 0.0) < 0.001;
        assert killMonsterNode.get("MonsterCd").asInt() == 5001;
        assert killMonsterNode.get("MonsterId").asInt() == 999888;
        assert killMonsterNode.get("Category").asInt() == 2;
        System.out.println("✓ KillMonster event serialization test passed");

        // Test object reset functionality
        login.reset(2, 54321, "aos");
        String resetLoginJson = login.serialize();
        System.out.println("Reset Login JSON: " + resetLoginJson);

        JsonNode resetLoginNode = mapper.readTree(resetLoginJson);
        assert resetLoginNode.get("ServerNo").asInt() == 2;
        assert resetLoginNode.get("AcntId").asInt() == 54321;
        assert resetLoginNode.get("Platform").asText().equals("aos");
        System.out.println("✓ Object reset test passed");

        System.out.println("✓ Basic functionality tests completed");
    }

    private static void validateBasicStructure(JsonNode node, String expectedEvent) {
        // Every log object should have DateTime and Event fields
        assert node.has("DateTime") : "DateTime field is missing";
        assert node.has("Event") : "Event field is missing";
        assert node.get("Event").asText().equals(expectedEvent) :
            "Expected event " + expectedEvent + " but got " + node.get("Event").asText();

        // DateTime should be in ISO format
        String dateTime = node.get("DateTime").asText();
        assert dateTime.contains("T") : "DateTime should be in ISO format";
        assert dateTime.length() > 19 : "DateTime should include timezone information";
    }
}
