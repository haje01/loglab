#include <iostream>
#include <fstream>
#include <string>
#include <cassert>
#include <cstdlib>
#include <filesystem>
#include <gtest/gtest.h>

#include "loglab_foo.h"


TEST(StringTest, Serialize) {
    auto login = loglab_foo::Login(1, 10000, "ios");
    std::string a = "\"Event\":\"Login\",\"ServerNo\":1,\"AcntId\":10000,\"Platform\":\"ios\"}";
    std::string b = login.Serialize();
    EXPECT_NE(b.find(a), std::string::npos); // 문자열 포함 테스트 
}


TEST(StringTest, SerializeAfterReset) {
    auto login = loglab_foo::Login(1, 10000, "ios");
    login.Reset(2, 20000, "aos");
    std::string a = "\"Event\":\"Login\",\"ServerNo\":2,\"AcntId\":20000,\"Platform\":\"aos\"}";
    std::string b = login.Serialize();
    EXPECT_NE(b.find(a), std::string::npos); // 문자열 포함 테스트 
}
