function o(t,a){const r=new Map;return[...t,...a].forEach(e=>{r.set(e.id,e)}),Array.from(r.values()).sort((e,n)=>new Date(e.created_at)-new Date(n.created_at))}export{o as m};
