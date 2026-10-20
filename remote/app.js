const status=document.querySelector('#status'),screen=document.querySelector('#screen');
let busy=false,screenWidth=1080,screenHeight=1920,point=null;
async function send(body){
  try{const r=await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const value=await r.json();if(!r.ok)throw Error(value.error);status.textContent='Connected · Android control ready';await refresh();}
  catch(e){status.textContent=e.message;}
}
async function refresh(){
  if(busy)return;busy=true;
  try{const response=await fetch('/api/screen');if(!response.ok){const value=await response.json();throw Error(value.error);}const blob=await response.blob(),url=URL.createObjectURL(blob),next=new Image();
    next.onload=()=>{const previous=screen.src;screenWidth=next.naturalWidth;screenHeight=next.naturalHeight;screen.src=url;if(previous.startsWith('blob:'))URL.revokeObjectURL(previous);busy=false;};
    next.onerror=()=>{URL.revokeObjectURL(url);busy=false;status.textContent='Screen image unavailable. Try refresh.';};next.src=url;
  }catch(e){busy=false;status.textContent=e.message;}
}
function coordinates(event){const box=screen.getBoundingClientRect();return {x:Math.round((event.clientX-box.left)*screenWidth/box.width),y:Math.round((event.clientY-box.top)*screenHeight/box.height)};}
document.querySelectorAll('[data-key]').forEach(b=>b.onclick=()=>send({action:'key',key:b.dataset.key}));
document.querySelectorAll('[data-app]').forEach(b=>b.onclick=()=>send({action:'app',app:b.dataset.app}));
document.querySelector('#refresh').onclick=refresh;
document.querySelector('#text-form').onsubmit=event=>{event.preventDefault();const input=document.querySelector('#text'),text=input.value;input.value='';if(text)void send({action:'text',text});};
screen.onpointerdown=e=>{if(!screen.src)return;point=coordinates(e);screen.setPointerCapture(e.pointerId);};
screen.onpointerup=e=>{if(!point)return;const end=coordinates(e),start=point;point=null;void send(Math.hypot(end.x-start.x,end.y-start.y)>25?{action:'swipe',...start,toX:end.x,toY:end.y}:{action:'tap',...end});};
screen.onpointercancel=()=>{point=null;};
setInterval(()=>{if(document.querySelector('#auto').checked&&!document.hidden)void refresh();},3000);
fetch('/api/status').then(r=>r.json()).then(v=>{status.textContent=v.error||'Connected · '+v.serial;}).catch(()=>{status.textContent='Remote unavailable';});
void refresh();
