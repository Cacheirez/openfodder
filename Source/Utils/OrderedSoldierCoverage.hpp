// GPL-3.0-or-later. Opt-in transaction evidence, never visual acceptance.
#pragma once
#include "OrderedSoldierArt.hpp"
#include <cstdio>
#include <cstdlib>
#include <string>
namespace openfodder {
class OrderedSoldierCoverage {
    struct Row {size_t order; std::string key; SoldierArtDecision decision;};
    const MissionLayerSequence& scene;
    PresentationDestinationId destination;
    unsigned density;
    bool enabled;
    uint64_t attempt = 0;
    const char* outcome = "interrupted";
    std::vector<Row> rows;
public:
    OrderedSoldierCoverage(const MissionLayerSequence& input,
            PresentationDestinationId target,unsigned scale)
        :scene(input),destination(target),density(scale) {
        const char* option=std::getenv("OPENFODDER_ORDERED_COVERAGE");
        enabled=option && std::string(option)=="1";
        if(enabled)attempt=NextPresentationSerial();
    }
    void resolved(size_t order,const std::string& key,SoldierArtDecision decision) {
        if(enabled)rows.push_back({order,key,decision});
    }
    void finish(const char* result) noexcept {outcome=result;}
    ~OrderedSoldierCoverage() noexcept {
        if(!enabled)return;
        size_t expected=0,replace=0,keep=0,missing=0;
        for(const auto& layer:scene.layers)
            if(layer.destination==destination && layer.operation==MissionLayerOperation::Soldier)++expected;
        for(const auto& row:rows){
            const auto& s=scene.layers[row.order].soldier.soldier;
            const char* decision=row.decision==SoldierArtDecision::Replace?"replace":
                row.decision==SoldierArtDecision::KeepClassic?"keep":"missing";
            if(row.decision==SoldierArtDecision::Replace)++replace;
            else if(row.decision==SoldierArtDecision::KeepClassic)++keep;
            else ++missing;
            std::fprintf(stderr,"SOLDIER_ORDERED_COMMAND: attempt=%llu scene=%llu interval=%llu order=%zu "
                "slot=%zu generation=%llu type=%d sheet=%d frame=%d key=%s decision=%s density=%u\n",
                (unsigned long long)attempt,(unsigned long long)s.scene,(unsigned long long)s.interval,
                row.order,s.slot,(unsigned long long)s.generation,int(s.type),int(s.sheet),int(s.frame),
                row.key.c_str(),decision,density);
        }
        // A replace decision counts as published only after the SDL transaction
        // succeeds. Partial census, missing art and recovered classic stay distinct.
        std::fprintf(stderr,"SOLDIER_ORDERED_RESULT: attempt=%llu outcome=%s expected=%zu observed=%zu "
            "replace=%zu keep=%zu missing=%zu density=%u\n",(unsigned long long)attempt,outcome,
            expected,rows.size(),replace,keep,missing,density);
    }
    OrderedSoldierCoverage(const OrderedSoldierCoverage&)=delete;
    OrderedSoldierCoverage& operator=(const OrderedSoldierCoverage&)=delete;
};
} // namespace openfodder
