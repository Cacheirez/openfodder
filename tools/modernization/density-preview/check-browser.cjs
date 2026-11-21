// GPL-3.0-or-later. Run the actual bundled page, including image decode and canvas.
'use strict';
const {chromium}=require('playwright');
const assert=require('assert/strict'),path=require('path'),fs=require('fs');
const {pathToFileURL}=require('url');
(async()=>{
 const root=path.resolve(__dirname,'../../..'),out=path.join(root,'reports/density-review');
 fs.mkdirSync(out,{recursive:true});
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try {
  for(const dpr of [1,3]){
   const page=await browser.newPage({viewport:{width:1200,height:1000},deviceScaleFactor:dpr});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(pathToFileURL(path.join(root,'assets/modernization/density-review/C01_DENSIDADES.html')).href);
   await page.waitForSelector('html[data-ready="true"]');
   for(const resolution of ['1920,1080','2560,1440','3840,2160'])for(const platform of ['200','225']){
    await page.selectOption('#resolution',resolution);await page.selectOption('#platform',platform);
    const sizes=await page.evaluate(()=>[8,12].map(d=>{
     const c=document.getElementById('real'+d);return {w:c.width,h:c.height,css:c.getBoundingClientRect().width,dpr:devicePixelRatio};
    }));
    assert.equal(sizes[0].w,sizes[1].w);assert.equal(sizes[0].h,sizes[1].h);
    for(const s of sizes)assert(Math.abs(s.css*s.dpr-s.w)<.1);
   }
   await page.selectOption('#platform','200');await page.selectOption('#guides','off');
   for(const background of ['ground','light','dark','checker']){
    await page.selectOption('#background',background);
    const different=await page.evaluate(()=>document.getElementById('real8').toDataURL()!==document.getElementById('real12').toDataURL());
    assert(different,'Different densities must actually render different detail at UHD');
   }
   // An oversized inspection canvas must scroll from its left edge, not be
   // centered into an unreachable negative overflow region.
   await page.selectOption('#zoom','4');
   const visibleLeft=await page.evaluate(()=>{const c=document.getElementById('zoom8');return c.getBoundingClientRect().left>=c.parentElement.getBoundingClientRect().left;});
   assert(visibleLeft);await page.selectOption('#zoom','2');
   await page.selectOption('#background','light');
   await page.screenshot({path:path.join(out,`C01-dpr${dpr}.png`),fullPage:true});
   assert.deepEqual(errors,[]);await page.close();
  }
  console.log('PASS: standalone page loads offline; 1080/1440/UHD PC/Amiga at DPR 1/3; equal physical footprints; distinct rendered densities; four backgrounds; no page errors');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
