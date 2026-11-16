// Quadros PNG com fundo transparente (para sobrepor em vídeo real). Uso: node render_alpha.js <html> <pasta> <dur> [fps]
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const [f,dir,dur,fps='30']=process.argv.slice(2);fs.mkdirSync(dir,{recursive:true});const N=Math.round(+dur*+fps);
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+path.resolve(f));await p.evaluate(()=>document.fonts.ready);
 for(let i=0;i<N;i++){await p.evaluate(t=>R(t),i/ +fps);await p.screenshot({path:`${dir}/${String(i).padStart(4,'0')}.png`,omitBackground:true})}
 await b.close();console.log('ok',dir)})();
