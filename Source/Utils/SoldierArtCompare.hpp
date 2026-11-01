// GPL-3.0-or-later. Opt-in snapshot of a genuinely published C01 composition.
#pragma once
#include "SoldierArtHDLayers.hpp"
#include <fstream>
#include <cstdlib>
#include <cstdio>
#include <cstring>
namespace openfodder {
inline bool SaveSoldierComparisonBitmap(const std::string& path,
        const std::vector<uint32_t>& pixels,int width,int height) {
    auto surface=SDL_CreateSurfaceFrom(width,height,SDL_PIXELFORMAT_XRGB8888,
        const_cast<uint32_t*>(pixels.data()),width*4);
    if(!surface)return false;
    const bool saved=SDL_SaveBMP(surface,path.c_str());
    SDL_DestroySurface(surface);return saved;
}
inline void SaveSoldierArtComparison(const MissionLayerSequence& scene,
        const PresentationDestinationId& destination,const SoldierArtHDLayers& frame,const SDL_FRect& src) {
    const char* enabled=std::getenv("OPENFODDER_HD_COMPARE");
    if(!enabled || std::string(enabled)!="1")return;
    static unsigned attempted=0;
    const unsigned bit=frame.density==12?2:1;
    if(attempted&bit)return;
    attempted|=bit; // At most one export attempt per density, never per frame.
    try {
        const auto classic=RasterizeMissionLayers(scene,destination);
        const std::string prefix="C01_"+std::to_string(frame.density);
        if(!SaveSoldierComparisonBitmap(prefix+"_clasico.bmp",classic.pixels,int(classic.width),int(classic.height)) ||
           !SaveSoldierComparisonBitmap(prefix+"_fondo.bmp",frame.background.pixels,int(classic.width),int(classic.height)) ||
           !SaveSoldierComparisonBitmap(prefix+"_parche.bmp",frame.patch,16*frame.density,14*frame.density)) {
            std::fprintf(stderr,"SOLDIER_HD_COMPARE: export failed (BMP): %s\n",SDL_GetError());return;
        }
        std::ofstream html(prefix+".html",std::ios::binary);
        html<<R"HTML(<!doctype html><html lang="es"><meta charset="utf-8">
<title>C01: escena real, clasico y HD</title>
<style>body{background:#17201d;color:#eef3eb;font:18px system-ui;margin:24px auto;max-width:1100px;padding:0 20px}button{font:inherit;padding:12px;cursor:pointer}canvas{image-rendering:pixelated;max-width:100%;height:auto;border:1px solid #809080}section{display:flex;gap:24px;flex-wrap:wrap}h1{font-size:28px}small{color:#c7d1c5}#error{color:#ffb8a0}</style>
<h1>C01: comparacion de una escena real</h1>
<p id="info"></p><p>El parche HD se publico en el juego antes de guardar esta captura. No es una recreacion: ambos lados usan el mismo instante, fondo y anclaje.</p>
<button id="toggle">Mostrar HD</button><p id="mode">Escena: clasico</p><canvas id="scene"></canvas>
<section><div><h2>Clasico ampliado</h2><canvas id="old"></canvas></div><div><h2>C01 HD ampliado</h2><canvas id="hd"></canvas></div></section>
<p><small>Ampliacion de inspeccion de una pose 16 x 14. La densidad del recurso no cambia el tamano del soldado en el juego. Esta pagina compara los pixeles de composicion guardados; no mide FPS ni captura el escalado final de la GPU. Conservar los tres BMP junto al HTML.</small></p><p id="error"></p>
<script>
)HTML";
        html<<"const prefix='"<<prefix<<"',x="<<frame.logicalX<<",y="<<frame.logicalY
            <<",density="<<frame.density<<",sceneId="<<frame.scene
            <<",sx="<<src.x<<",sy="<<src.y<<",sw="<<src.w<<",sh="<<src.h<<";\n";
        html<<R"HTML(const load=s=>new Promise((ok,bad)=>{const i=new Image;i.onload=()=>ok(i);i.onerror=bad;i.src=prefix+s+'.bmp'});
Promise.all(['_clasico','_fondo','_parche'].map(load)).then(([classic,bg,patch])=>{
document.getElementById('info').textContent=`Densidad ${density}x | escena ${sceneId} | anclaje (${x}, ${y})`;
const full=document.getElementById('scene');full.width=Math.round(sw*2);full.height=Math.round(sh*2);
let modern=false;function draw(){const c=full.getContext('2d');c.imageSmoothingEnabled=false;c.drawImage(modern?bg:classic,sx,sy,sw,sh,0,0,full.width,full.height);if(modern)c.drawImage(patch,(x-sx)*2,(y-sy)*2,32,28);c.strokeStyle='#ffd76b';c.strokeRect((x-sx)*2-2,(y-sy)*2-2,36,32);document.getElementById('mode').textContent='Escena: '+(modern?'HD':'clasico');document.getElementById('toggle').textContent=modern?'Mostrar clasico':'Mostrar HD'}draw();
document.getElementById('toggle').onclick=()=>{modern=!modern;draw()};
for(const id of ['old','hd']){const canvas=document.getElementById(id);canvas.width=384;canvas.height=336;const c=canvas.getContext('2d');c.imageSmoothingEnabled=false;if(id==='old')c.drawImage(classic,x,y,16,14,0,0,384,336);else c.drawImage(patch,0,0,384,336)}
}).catch(()=>document.getElementById('error').textContent='No se pudieron cargar los BMP. Extrae todos los archivos en la misma carpeta.');
</script></html>)HTML";
        html.close();
        std::fprintf(stderr,html?"SOLDIER_HD_COMPARE: saved %s.html\n":"SOLDIER_HD_COMPARE: export failed (HTML): %s\n",prefix.c_str());
    } catch(const std::exception& e) {
        // Diagnostic IO/allocation failures must not undo a successful draw.
        std::fprintf(stderr,"SOLDIER_HD_COMPARE: export failed: %s\n",e.what());
    }
}
} // namespace openfodder
