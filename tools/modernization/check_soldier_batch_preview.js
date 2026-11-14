const fs=require('fs'),vm=require('vm'),assert=require('assert');
const {createCanvas,ImageData}=require('@napi-rs/canvas');
const html=fs.readFileSync(process.argv[2],'utf8');
const els={left:createCanvas(192,168),right:createCanvas(192,168),pose:{},pause:{},speed:{value:'180'}};
let callback;const ctx=vm.createContext({document:{getElementById:k=>els[k]},ImageData,Uint8ClampedArray,atob:s=>Buffer.from(s,'base64').toString('binary'),requestAnimationFrame:f=>{callback=f;}});
vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],ctx);
const sheet=createCanvas(576,336),c=sheet.getContext('2d');c.fillStyle='#354638';c.fillRect(0,0,576,336);
let snapshots=[];
for(const t of [0,180,360,540]){if(t)callback(t);snapshots.push(els.left.toBuffer('image/png'));if(t<540){c.drawImage(els.left,t/180*192,0);c.drawImage(els.right,t/180*192,168);}}
assert(!snapshots[0].equals(snapshots[1]));assert(!snapshots[1].equals(snapshots[2]));assert(snapshots[1].equals(snapshots[3]));
els.pause.onclick();callback(1000);assert(els.pause.textContent==='Reanudar');assert(els.pose.textContent==='Pose 1');els.pause.onclick();callback(1200);assert(els.pose.textContent==='Pose 0');
fs.writeFileSync(process.argv[3],sheet.toBuffer('image/png'));console.log('PASS preview: six derivative buffers; 0-1-2-1; pause/resume; exact pixel output (Skia, not browser/GPU)');
