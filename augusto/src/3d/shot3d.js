const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:1100,height:1950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
for(const id of process.argv.slice(2)){await p.goto('http://127.0.0.1:8765/scene.html?p='+id);await p.waitForFunction(()=>window.READY,null,{timeout:120000});await p.waitForTimeout(400);
await (await p.$('#art')).screenshot({path:'/tmp/claude-0/r3d/out_'+id+'.png'});console.log('ok',id)}
console.log(errs.join('\n'));await b.close()})();
