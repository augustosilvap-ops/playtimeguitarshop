// Uso: node render_motion.js <arquivo.html> <saida.mp4> [dur=10] [fps=30]
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');const {execFileSync}=require('child_process');
(async()=>{const [f,out,dur='10',fps='30']=process.argv.slice(2);const N=Math.round(+dur*+fps);
 const dir=fs.mkdtempSync('/tmp/mframes-');const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.goto('file://'+path.resolve(f));await p.evaluate(()=>document.fonts.ready);
 for(let i=0;i<N;i++){await p.evaluate(t=>R(t),i/ +fps);await p.screenshot({path:`${dir}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:94})}
 await b.close();
 execFileSync('ffmpeg',['-v','error','-y','-framerate',fps,'-i',`${dir}/%04d.jpg`,'-f','lavfi','-t',dur,'-i','anullsrc=r=48000:cl=stereo','-c:v','libx264','-profile:v','high','-preset','slow','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-shortest','-movflags','+faststart',out]);
 fs.rmSync(dir,{recursive:true});console.log('ok',out)})();
