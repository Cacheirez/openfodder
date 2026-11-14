// GPL-3.0-or-later. Browser-only inspection, original source remains untouched.
'use strict';
const fields=['resolution','platform','background','zoom','guides'];
const textures=new Map();
const source=new Image();
function paint(canvas,texture,geometry,zoom,dpr) {
  const sw=geometry.physicalWidth*zoom,sh=geometry.physicalHeight*zoom,pad=20;
  canvas.width=Math.ceil(sw)+2*pad;canvas.height=Math.ceil(sh)+2*pad;
  canvas.style.width=(canvas.width/dpr)+'px';canvas.style.height=(canvas.height/dpr)+'px';
  const c=canvas.getContext('2d'),background=document.getElementById('background').value;
  c.fillStyle=({light:'#e8e1cb',dark:'#16221c',ground:'#777650',checker:'#c2c5bd'})[background];c.fillRect(0,0,canvas.width,canvas.height);
  if(background==='checker'){c.fillStyle='#868f84';for(let y=0;y<canvas.height;y+=16)for(let x=0;x<canvas.width;x+=16)if(((x+y)/16)%2===0)c.fillRect(x,y,16,16);}
  c.imageSmoothingEnabled=true;c.imageSmoothingQuality='high';
  c.drawImage(texture,pad,pad,sw,sh);
  if(document.getElementById('guides').value==='on'){
    c.strokeStyle='#ccedb0';c.lineWidth=1;c.setLineDash([3,3]);c.strokeRect(pad,pad,sw,sh);c.setLineDash([]);
    const ax=pad+sw/2,ay=pad+sh;c.strokeStyle='#fff';c.beginPath();c.moveTo(ax-5,ay);c.lineTo(ax+5,ay);c.moveTo(ax,ay-5);c.lineTo(ax,ay+5);c.stroke();
  }
}
function refresh(){
  if(textures.size!==2)return;
  const [w,h]=document.getElementById('resolution').value.split(',').map(Number),lh=Number(document.getElementById('platform').value);
  const dpr=window.devicePixelRatio||1,g=DensityReview.layout(w,h,lh,dpr),zoom=Number(document.getElementById('zoom').value);
  for(const density of [8,12]){paint(document.getElementById('real'+density),textures.get(density),g,1,dpr);paint(document.getElementById('zoom'+density),textures.get(density),g,zoom,dpr);}
  document.getElementById('status').textContent='C01 cargado · misma pose y anclaje · ampliación de inspección '+zoom+'×';
  document.getElementById('geometry').textContent=`Cuadro lógico 16 × 14 → ${g.physicalWidth.toFixed(2)} × ${g.physicalHeight.toFixed(2)} píxeles físicos. Escala ${g.scale.toFixed(2)}×; DPR navegador ${dpr.toFixed(2)}. El recurso 8× se presenta a ${(g.scale/8).toFixed(3)}× y el 12× a ${(g.scale/12).toFixed(3)}× de su resolución. Sin decidir cuál es mejor.`;
  document.documentElement.dataset.ready='true';
}
source.onload=()=>{
  try {
    const canvas=document.createElement('canvas');canvas.width=source.naturalWidth;canvas.height=source.naturalHeight;
    const context=canvas.getContext('2d',{willReadFrequently:true});context.drawImage(source,0,0);
    const pixels=context.getImageData(0,0,canvas.width,canvas.height).data;
    for(const density of [8,12]){const prepared=DensityReview.prepare(pixels,canvas.width,canvas.height,density);
      const texture=document.createElement('canvas');texture.width=prepared.width;texture.height=prepared.height;
      texture.getContext('2d').putImageData(new ImageData(prepared.pixels,prepared.width,prepared.height),0,0);textures.set(density,texture);}
    refresh();
  } catch(error){document.getElementById('status').textContent='No se puede preparar la comparación: '+error.message;}
};
source.onerror=()=>{document.getElementById('status').textContent='No se encuentra source.png. Sirve la raíz del repositorio con python -m http.server 8000 y abre /tools/modernization/density-preview/.';};
for(const id of fields)document.getElementById(id).addEventListener('change',refresh);
window.addEventListener('resize',refresh);
source.src='../../../assets/modernization/soldier-c01/source.png';
