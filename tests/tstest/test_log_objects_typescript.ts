#!/usr/bin/env node
/**
 * Basic tests for TypeScript log objects generated from foo.lab.json
 */

import { Login, Logout, KillMonster, CharLogin, GetItem } from './loglab_foo';

function testBasicLogObjects(): void {
    console.log('Testing basic log object functionality...');

    // Test Login event
    const login = new Login(1, 10000, "ios");
    login.AcntId = 12345;
    login.ServerNo = 1;
    login.Platform = "ios";

    // Test serialization
    const loginJson = login.serialize();
    const loginData = JSON.parse(loginJson);

    console.assert(loginData.AcntId === 12345, 'Login AcntId should be 12345');
    console.assert(loginData.ServerNo === 1, 'Login ServerNo should be 1');
    console.assert(loginData.Platform === "ios", 'Login Platform should be ios');
    console.assert('DateTime' in loginData, 'Login should have DateTime field');
    console.assert(loginData.Category === 1, 'Login Category should be 1');
    console.assert(loginData.Event === "Login", 'Event should be Login');

    // Test Logout event with optional field
    const logout = new Logout(1, 10000);
    logout.AcntId = 12345;
    logout.ServerNo = 1;
    logout.PlayTime = 3600.5;

    const logoutJson = logout.serialize();
    const logoutData = JSON.parse(logoutJson);

    console.assert(logoutData.AcntId === 12345, 'Logout AcntId should be 12345');
    console.assert(logoutData.PlayTime === 3600.5, 'Logout PlayTime should be 3600.5');
    console.assert(logoutData.Event === "Logout", 'Event should be Logout');

    // Test KillMonster event with many parameters
    const killMonster = new KillMonster(1, 1234, 5678, 1001, 100.5, 200.7, 0.0, 5001, 999888);
    const killJson = killMonster.serialize();
    const killData = JSON.parse(killJson);

    console.assert(killData.CharId === 5678, 'KillMonster CharId should be 5678');
    console.assert(killData.MonsterCd === 5001, 'KillMonster MonsterCd should be 5001');
    console.assert(killData.PosX === 100.5, 'KillMonster PosX should be 100.5');
    console.assert(killData.Event === "KillMonster", 'Event should be KillMonster');

    // Test reset functionality
    login.reset(2, 20000, "aos");
    const loginResetJson = login.serialize();
    const loginResetData = JSON.parse(loginResetJson);

    console.assert(loginResetData.AcntId === 20000, 'Reset Login AcntId should be 20000');
    console.assert(loginResetData.ServerNo === 2, 'Reset Login ServerNo should be 2');
    console.assert(loginResetData.Platform === "aos", 'Reset Login Platform should be aos');

    console.log('✓ Basic log object tests passed');
}

function testOptionalFields(): void {
    console.log('Testing optional field handling...');

    // Test Logout without optional PlayTime
    const logout = new Logout(1, 10000);
    const logoutJson = logout.serialize();
    const logoutData = JSON.parse(logoutJson);

    console.assert(logout.PlayTime === null, 'PlayTime should be null initially');
    console.assert(!('PlayTime' in logoutData), 'PlayTime should not be in serialized data when null');

    // Test Logout with optional PlayTime
    logout.PlayTime = 1234.5;
    const logoutWithTimeJson = logout.serialize();
    const logoutWithTimeData = JSON.parse(logoutWithTimeJson);

    console.assert('PlayTime' in logoutWithTimeData, 'PlayTime should be in serialized data when not null');
    console.assert(logoutWithTimeData.PlayTime === 1234.5, 'PlayTime should be 1234.5');

    console.log('✓ Optional field tests passed');
}

function testTypeScriptFeatures(): void {
    console.log('Testing TypeScript-specific features...');

    // Test readonly Event property
    const login = new Login(1, 10000, "ios");
    console.assert(login.Event === "Login", 'Event property should be "Login"');

    // Test type checking (this will be caught at compile time)
    // login.Event = "SomeOtherEvent"; // This should cause a TypeScript error

    // Test null union types for optional fields
    const logout = new Logout(1, 10000);
    logout.PlayTime = null; // This should be valid
    logout.PlayTime = 123.45; // This should also be valid
    // logout.PlayTime = "invalid"; // This should cause a TypeScript error

    console.log('✓ TypeScript feature tests passed');
}

function testJsonOutput(): void {
    console.log('Testing JSON output format...');

    const login = new Login(1, 12345, "ios");
    const json = login.serialize();
    const data = JSON.parse(json);

    // Check required fields
    const requiredFields = ['DateTime', 'Event', 'ServerNo', 'AcntId', 'Category', 'Platform'];
    for (const field of requiredFields) {
        console.assert(field in data, `Required field ${field} should be in JSON output`);
    }

    // Check DateTime format (ISO string)
    const dateTime = new Date(data.DateTime);
    console.assert(!isNaN(dateTime.getTime()), 'DateTime should be a valid date string');

    console.log('✓ JSON output tests passed');
}

function main(): void {
    try {
        testBasicLogObjects();
        testOptionalFields();
        testTypeScriptFeatures();
        testJsonOutput();
        console.log('\n🎉 All TypeScript tests passed!');
    } catch (error) {
        console.error('\n❌ Test failed:', error);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}
