// Usage: node render.js "Votre phrase" sortie.png
const {chromium}=require('playwright');const path=require('path');
(async()=>{const [text,out='sortie.png']=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
const u='file://'+path.join(__dirname,'template.html')+(text?'?t='+encodeURIComponent(text):'');
await p.goto(u);await p.evaluate(()=>document.fonts.ready);
await p.screenshot({path:out});await b.close();})();
