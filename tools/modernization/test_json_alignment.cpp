// Regression for MSVC x86 by-value JSON/callback alignment.
#ifdef NDEBUG
#undef NDEBUG
#endif
#include "Utils/json.hpp"
#include <sstream>
#include <cassert>
#include <utility>
int main() {
 using J=nlohmann::json;
 std::istringstream in("{\"x\":1,\"a\":[null,true,2.5,\"s\",{\"n\":-4}]}");
 J a; in>>a; assert(a.at("x").get<int>()==1); assert(a["a"][2].get<double>()==2.5);
 J b; b=a; assert(b==a); b["x"]=7; assert(a["x"]==1);
 b=b; assert(b["x"]==7);
 J c; c=std::move(b); assert(c["x"]==7 && b.is_null());
 c=std::move(c); assert(c["x"]==7);
 J d; d=a["a"]; assert(d.is_array() && d.size()==5);
 J round=J::parse(a.dump()); assert(round==a);
 int calls=0; J::parser_callback_t cb=[&](int,J::parse_event_t,J&){++calls;return true;}; J parsed=J::parse(a.dump(),cb); assert(parsed==a && calls>0);
 bool caught=false; try { J::parse("{bad}"); } catch(const J::parse_error&) { caught=true; } assert(caught);
}
