// GPL-3.0-or-later. Model regression; browser rendering is checked separately.
'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const {prepare,layout}=require('./model.js');
const raw=fs.readFileSync(process.argv[2]),root=process.argv[3];
const header=fs.readFileSync(path.join(root,'Source/Utils/SoldierArtPixels.hpp'),'utf8');
const packed=[...header.matchAll(/(\d+)u,/g)].map(x=>Number(x[1]));
const native=prepare(raw,1353,1162,1);assert.equal(packed.length,224);
for(let i=0;i<224;i++) {const j=4*i,value=((native.pixels[j+3]<<24)|(native.pixels[j]<<16)|(native.pixels[j+1]<<8)|native.pixels[j+2])>>>0;assert.equal(value,packed[i]);}
for(const d of [8,12]) {
 const p=prepare(raw,1353,1162,d);assert.equal(p.width,16*d);assert.equal(p.height,14*d);
 assert.deepEqual(p.anchor,[8*d,14*d]);assert.equal(p.pixels.length,16*14*4*d*d);
 assert.deepEqual(p.pixels,prepare(raw,1353,1162,d).pixels);
 let opaque=0;
 for(let y=0;y<p.height;y++)for(let x=0;x<p.width;x++){
  const a=p.pixels[4*(y*p.width+x)+3];if(x<3*d||x>=13*d)assert.equal(a,0);opaque+=a>0;
 }assert(opaque>0);
}
// Invisible fringe cannot tint visible pixels. Uniform opaque color is conserved.
const solid=Buffer.alloc(raw.length);
for(let i=0;i<solid.length;i+=4){solid[i]=190;solid[i+1]=70;solid[i+2]=20;solid[i+3]=15;}
assert(prepare(solid,1353,1162,8).pixels.every(x=>x===0));
for(let i=3;i<solid.length;i+=4)solid[i]=255;
for(const d of [8,12]){const p=prepare(solid,1353,1162,d);for(let y=0;y<p.height;y++)for(let x=3*d;x<13*d;x++)assert.deepEqual(Array.from(p.pixels.slice(4*(y*p.width+x),4*(y*p.width+x)+4)),[190,70,20,255]);}
let count=0;
for(const [w,h]of [[1280,720],[1920,1080],[2560,1440],[3840,2160],[640,480],[1280,960],[1920,1440],[2880,2160]])
 for(const logical of [200,225])for(const dpr of [1,1.25,1.5,1.75,2,3]){
 const g=layout(w,h,logical,dpr);assert(g.viewport.x>=0&&g.viewport.y>=0);
 assert(Math.abs(g.cssWidth*dpr-g.physicalWidth)<1e-9);
 assert(Math.abs(g.physicalWidth/g.physicalHeight-16/14)<1e-9);
 assert(Math.abs(2*g.viewport.x+g.viewport.width-w)<1e-9);count++;
 }
assert.equal(layout(3840,2160,200,3).scale,10.8);
assert.equal(layout(3840,2160,225,3).scale,9.6);
for(const d of [0,-1,2,Infinity,NaN])assert.throws(()=>prepare(raw,1353,1162,d));
assert.throws(()=>prepare(raw,1352,1162,8));
for(const dpr of [0,-1,NaN,Infinity])assert.throws(()=>layout(1920,1080,200,dpr));
console.log(`PASS: exact native C01 equivalence; deterministic 8/12, alpha, bounds, anchors; ${count} output/platform/DPR cases; invalid input rejection`);
