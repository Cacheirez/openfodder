// GPL-3.0-or-later. Geometry of one presented scene, independent of SDL/assets.
#pragma once
#include <cmath>
namespace openfodder {
struct ScreenPoint { double x=0, y=0; };
struct ScreenRect { double x=0, y=0, w=0, h=0; };
struct ScreenTransform {
    bool valid=false;
    int windowW=0,windowH=0,outputW=0,outputH=0;
    ScreenRect source, destination;
    static bool RectValid(const ScreenRect& r) {
        return std::isfinite(r.x) && std::isfinite(r.y) &&
            std::isfinite(r.w) && std::isfinite(r.h) && r.w>0 && r.h>0;
    }
    // Preserve the accepted windowed pixel proportions (no new aspect correction).
    static ScreenRect FitSource(int pw,int ph,ScreenRect src) {
        if(pw<=0 || ph<=0 || !RectValid(src)) return {};
        const double scale=std::fmin(double(pw)/src.w,double(ph)/src.h);
        const double w=src.w*scale,h=src.h*scale;
        return {(pw-w)/2,(ph-h)/2,w,h};
    }
    static ScreenTransform FromDraw(int ww,int wh,int pw,int ph,
                                    ScreenRect src,ScreenRect dst) {
        ScreenTransform t;
        if(ww<=0 || wh<=0 || pw<=0 || ph<=0 || !RectValid(src) || !RectValid(dst) ||
           src.x<0 || src.y<0 || dst.x<0 || dst.y<0 ||
           dst.x+dst.w>pw || dst.y+dst.h>ph) return t;
        t.valid=true;t.windowW=ww;t.windowH=wh;t.outputW=pw;t.outputH=ph;
        t.source=src;t.destination=dst;return t;
    }
    ScreenPoint CanvasToOutput(ScreenPoint p) const {
        return {destination.x+p.x*destination.w/source.w,
                destination.y+p.y*destination.h/source.h};
    }
    ScreenPoint StorageToOutput(ScreenPoint p) const {
        return CanvasToOutput({p.x-source.x,p.y-source.y});
    }
    bool WindowToCanvas(ScreenPoint p,ScreenPoint& result) const {
        if(!valid || !std::isfinite(p.x) || !std::isfinite(p.y))return false;
        const double x=p.x*outputW/windowW,y=p.y*outputH/windowH;
        if(x<destination.x || y<destination.y ||
           x>=destination.x+destination.w || y>=destination.y+destination.h)return false;
        result={(x-destination.x)*source.w/destination.w,
                (y-destination.y)*source.h/destination.h};
        return true;
    }
    ScreenPoint CanvasToWindow(ScreenPoint p) const {
        const auto physical=CanvasToOutput(p);
        return {physical.x*windowW/outputW,physical.y*windowH/outputH};
    }
};
enum class ScreenMouseResult { Classic, Blocked, Mapped };
}
