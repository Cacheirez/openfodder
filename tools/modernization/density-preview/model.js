// GPL-3.0-or-later. Offline review model; never imported by the game.
(function (root) {
  'use strict';
  const contract = Object.freeze({width:1353,height:1162,left:406,top:176,right:969,bottom:1026,
    frameWidth:16,frameHeight:14,contentLeft:3,contentRight:13,feetX:8,feetY:14,alphaMin:16});
  // Same integer bins, alpha threshold and premultiplied area average as
  // build_soldier_art.cpp. Density 1 must reproduce the checked-in native body.
  function prepare(pixels, width, height, density) {
    if(width!==contract.width || height!==contract.height || pixels.length!==width*height*4)
      throw new Error('C01 source dimensions do not match the preserved contract');
    if(![1,8,12].includes(density)) throw new Error('Review supports only 1, 8 and 12');
    const w=16*density,h=14*density,out=new Uint8ClampedArray(w*h*4),cw=10*density;
    for(let y=0;y<h;y++) for(let x=3*density;x<13*density;x++) {
      const x0=406+Math.floor((x-3*density)*563/cw),x1=406+Math.floor((x-3*density+1)*563/cw);
      const y0=176+Math.floor(y*850/h),y1=176+Math.floor((y+1)*850/h);
      let a=0,r=0,g=0,b=0;
      for(let sy=y0;sy<y1;sy++) for(let sx=x0;sx<x1;sx++) {
        const i=4*(sy*width+sx),alpha=pixels[i+3]>=16?pixels[i+3]:0;
        a+=alpha;r+=pixels[i]*alpha;g+=pixels[i+1]*alpha;b+=pixels[i+2]*alpha;
      }
      if(a) {const i=4*(y*w+x);out[i]=Math.floor(r/a);out[i+1]=Math.floor(g/a);
        out[i+2]=Math.floor(b/a);out[i+3]=Math.floor(a/((x1-x0)*(y1-y0)));}
    }
    return {width:w,height:h,pixels:out,density,anchor:[8*density,14*density]};
  }
  function layout(outputWidth,outputHeight,logicalHeight,dpr=1) {
    if(![outputWidth,outputHeight,logicalHeight,dpr].every(x=>Number.isFinite(x)&&x>0))
      throw new Error('Positive finite geometry required');
    if(![200,225].includes(logicalHeight)) throw new Error('Choose PC 200 or Amiga 225');
    const scale=Math.min(outputWidth/320,outputHeight/logicalHeight);
    return {scale,physicalWidth:16*scale,physicalHeight:14*scale,
      cssWidth:16*scale/dpr,cssHeight:14*scale/dpr,
      viewport:{x:(outputWidth-320*scale)/2,y:(outputHeight-logicalHeight*scale)/2,
        width:320*scale,height:logicalHeight*scale}};
  }
  const api={contract,prepare,layout};
  if(typeof module!=='undefined') module.exports=api; else root.DensityReview=api;
})(typeof globalThis!=='undefined'?globalThis:this);
