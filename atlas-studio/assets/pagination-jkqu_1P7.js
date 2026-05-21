import{F as K}from"./index.es-BikRAUgq.js";import{E as re}from"./index-C0ecZP0d.js";import{d as B,x as N,y as U,C as P,D as k,q as m,G as se,H as T,E as S,Q as I,F as E,K as oe,N as V,O as X,J as F,I as le,z as ie,n as ce}from"./vendor-vue-NSDaktjZ.js";import{H,bq as pe,B as de,Y as he,X as ue}from"./index-CHY6HOcZ.js";import{h as fe}from"./highlight-BaR19uYO.js";import"./vendor-highlight-lEWW1Jxd.js";import{E as ge}from"./index-C3GxuMzd.js";import{E as ye}from"./index-17hcxsGI.js";const ve=B({name:"InfoIcon",components:{FontAwesomeIcon:K,ElTooltip:re},props:{content:{type:String,required:!0}}});function me(e,t,n,a,s,o){const l=k("font-awesome-icon"),i=k("el-tooltip");return m(),N(i,{effect:"dark",content:e.content,placement:"top"},{default:U(()=>[P(l,{icon:"fa-solid fa-info",class:"icon icon-rotate inline-block w-[20px] h-[20px] border-[3px] border-solid border-[var(--el-text-color-placeholder)] rounded-full text-[10px] p-[5px] scale-[0.4] cursor-pointer text-[var(--el-text-color-placeholder)] -mr-[5px]"})]),_:1},8,["content"])}const jt=H(ve,[["render",me]]);var we=Object.prototype.toString,x=Array.isArray||function(t){return we.call(t)==="[object Array]"};function D(e){return typeof e=="function"}function Ce(e){return x(e)?"array":typeof e}function z(e){return e.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g,"\\$&")}function W(e,t){return e!=null&&typeof e=="object"&&t in e}function be(e,t){return e!=null&&typeof e!="object"&&e.hasOwnProperty&&e.hasOwnProperty(t)}var ke=RegExp.prototype.test;function Te(e,t){return ke.call(e,t)}var Ae=/\S/;function Se(e){return!Te(Ae,e)}var _e={"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;","/":"&#x2F;","`":"&#x60;","=":"&#x3D;"};function Le(e){return String(e).replace(/[&<>"'`=\/]/g,function(n){return _e[n]})}var Ee=/\s*/,Pe=/\s+/,J=/\s*=/,Re=/\s*\}/,xe=/#|\^|\/|>|\{|&|=|!/;function qe(e,t){if(!e)return[];var n=!1,a=[],s=[],o=[],l=!1,i=!1,r="",c=0;function h(){if(l&&!i)for(;o.length;)delete s[o.pop()];else o=[];l=!1,i=!1}var p,y,q;function $(v){if(typeof v=="string"&&(v=v.split(Pe,2)),!x(v)||v.length!==2)throw new Error("Invalid tags: "+v);p=new RegExp(z(v[0])+"\\s*"),y=new RegExp("\\s*"+z(v[1])),q=new RegExp("\\s*"+z("}"+v[1]))}$(t||C.tags);for(var d=new O(e),b,u,f,A,L,w;!d.eos();){if(b=d.pos,f=d.scanUntil(p),f)for(var _=0,M=f.length;_<M;++_)A=f.charAt(_),Se(A)?(o.push(s.length),r+=A):(i=!0,n=!0,r+=" "),s.push(["text",A,b,b+1]),b+=1,A===`
`&&(h(),r="",c=0,n=!1);if(!d.scan(p))break;if(l=!0,u=d.scan(xe)||"name",d.scan(Ee),u==="="?(f=d.scanUntil(J),d.scan(J),d.scanUntil(y)):u==="{"?(f=d.scanUntil(q),d.scan(Re),d.scanUntil(y),u="&"):f=d.scanUntil(y),!d.scan(y))throw new Error("Unclosed tag at "+d.pos);if(u==">"?L=[u,f,b,d.pos,r,c,n]:L=[u,f,b,d.pos],c++,s.push(L),u==="#"||u==="^")a.push(L);else if(u==="/"){if(w=a.pop(),!w)throw new Error('Unopened section "'+f+'" at '+b);if(w[1]!==f)throw new Error('Unclosed section "'+w[1]+'" at '+b)}else u==="name"||u==="{"||u==="&"?i=!0:u==="="&&$(f)}if(h(),w=a.pop(),w)throw new Error('Unclosed section "'+w[1]+'" at '+d.pos);return Ue($e(s))}function $e(e){for(var t=[],n,a,s=0,o=e.length;s<o;++s)n=e[s],n&&(n[0]==="text"&&a&&a[0]==="text"?(a[1]+=n[1],a[3]=n[3]):(t.push(n),a=n));return t}function Ue(e){for(var t=[],n=t,a=[],s,o,l=0,i=e.length;l<i;++l)switch(s=e[l],s[0]){case"#":case"^":n.push(s),a.push(s),n=s[4]=[];break;case"/":o=a.pop(),o[5]=s[2],n=a.length>0?a[a.length-1][4]:t;break;default:n.push(s)}return t}function O(e){this.string=e,this.tail=e,this.pos=0}O.prototype.eos=function(){return this.tail===""};O.prototype.scan=function(t){var n=this.tail.match(t);if(!n||n.index!==0)return"";var a=n[0];return this.tail=this.tail.substring(a.length),this.pos+=a.length,a};O.prototype.scanUntil=function(t){var n=this.tail.search(t),a;switch(n){case-1:a=this.tail,this.tail="";break;case 0:a="";break;default:a=this.tail.substring(0,n),this.tail=this.tail.substring(n)}return this.pos+=a.length,a};function R(e,t){this.view=e,this.cache={".":this.view},this.parent=t}R.prototype.push=function(t){return new R(t,this)};R.prototype.lookup=function(t){var n=this.cache,a;if(n.hasOwnProperty(t))a=n[t];else{for(var s=this,o,l,i,r=!1;s;){if(t.indexOf(".")>0)for(o=s.view,l=t.split("."),i=0;o!=null&&i<l.length;)i===l.length-1&&(r=W(o,l[i])||be(o,l[i])),o=o[l[i++]];else o=s.view[t],r=W(s.view,t);if(r){a=o;break}s=s.parent}n[t]=a}return D(a)&&(a=a.call(this.view)),a};function g(){this.templateCache={_cache:{},set:function(t,n){this._cache[t]=n},get:function(t){return this._cache[t]},clear:function(){this._cache={}}}}g.prototype.clearCache=function(){typeof this.templateCache<"u"&&this.templateCache.clear()};g.prototype.parse=function(t,n){var a=this.templateCache,s=t+":"+(n||C.tags).join(":"),o=typeof a<"u",l=o?a.get(s):void 0;return l==null&&(l=qe(t,n),o&&a.set(s,l)),l};g.prototype.render=function(t,n,a,s){var o=this.getConfigTags(s),l=this.parse(t,o),i=n instanceof R?n:new R(n,void 0);return this.renderTokens(l,i,a,t,s)};g.prototype.renderTokens=function(t,n,a,s,o){for(var l="",i,r,c,h=0,p=t.length;h<p;++h)c=void 0,i=t[h],r=i[0],r==="#"?c=this.renderSection(i,n,a,s,o):r==="^"?c=this.renderInverted(i,n,a,s,o):r===">"?c=this.renderPartial(i,n,a,o):r==="&"?c=this.unescapedValue(i,n):r==="name"?c=this.escapedValue(i,n,o):r==="text"&&(c=this.rawValue(i)),c!==void 0&&(l+=c);return l};g.prototype.renderSection=function(t,n,a,s,o){var l=this,i="",r=n.lookup(t[1]);function c(y){return l.render(y,n,a,o)}if(r){if(x(r))for(var h=0,p=r.length;h<p;++h)i+=this.renderTokens(t[4],n.push(r[h]),a,s,o);else if(typeof r=="object"||typeof r=="string"||typeof r=="number")i+=this.renderTokens(t[4],n.push(r),a,s,o);else if(D(r)){if(typeof s!="string")throw new Error("Cannot use higher-order sections without the original template");r=r.call(n.view,s.slice(t[3],t[5]),c),r!=null&&(i+=r)}else i+=this.renderTokens(t[4],n,a,s,o);return i}};g.prototype.renderInverted=function(t,n,a,s,o){var l=n.lookup(t[1]);if(!l||x(l)&&l.length===0)return this.renderTokens(t[4],n,a,s,o)};g.prototype.indentPartial=function(t,n,a){for(var s=n.replace(/[^ \t]/g,""),o=t.split(`
`),l=0;l<o.length;l++)o[l].length&&(l>0||!a)&&(o[l]=s+o[l]);return o.join(`
`)};g.prototype.renderPartial=function(t,n,a,s){if(a){var o=this.getConfigTags(s),l=D(a)?a(t[1]):a[t[1]];if(l!=null){var i=t[6],r=t[5],c=t[4],h=l;r==0&&c&&(h=this.indentPartial(l,c,i));var p=this.parse(h,o);return this.renderTokens(p,n,a,h,s)}}};g.prototype.unescapedValue=function(t,n){var a=n.lookup(t[1]);if(a!=null)return a};g.prototype.escapedValue=function(t,n,a){var s=this.getConfigEscape(a)||C.escape,o=n.lookup(t[1]);if(o!=null)return typeof o=="number"&&s===C.escape?String(o):s(o)};g.prototype.rawValue=function(t){return t[1]};g.prototype.getConfigTags=function(t){return x(t)?t:t&&typeof t=="object"?t.tags:void 0};g.prototype.getConfigEscape=function(t){if(t&&typeof t=="object"&&!x(t))return t.escape};var C={name:"mustache.js",version:"4.2.0",tags:["{{","}}"],clearCache:void 0,escape:void 0,parse:void 0,render:void 0,Scanner:void 0,Context:void 0,Writer:void 0,set templateCache(e){j.templateCache=e},get templateCache(){return j.templateCache}},j=new g;C.clearCache=function(){return j.clearCache()};C.parse=function(t,n){return j.parse(t,n)};C.render=function(t,n,a,s){if(typeof t!="string")throw new TypeError('Invalid template! Template should be a "string" but "'+Ce(t)+'" was given as the first argument for mustache#render(template, view, partials)');return j.render(t,n,a,s)};C.escape=Le;C.Scanner=O;C.Context=R;C.Writer=g;const je=B({name:"CodeSnippet",directives:{highlight:fe},props:{code:{type:String,required:!0},lang:{type:String,required:!1,default:""}},computed:{languageClass(){const e=(this.lang||"").toLowerCase();return e?`language-${{shell:"bash",bash:"bash",javascript:"javascript",js:"javascript",python:"python",py:"python",java:"java",go:"go",php:"php"}[e]||e}`:""}}}),Be={class:"code-snippet rounded-md overflow-hidden"};function He(e,t,n,a,s,o){const l=oe("highlight");return se((m(),T("div",Be,[S("pre",null,[S("code",{class:I(e.languageClass)},E(e.code),3)])])),[[l]])}const Oe=H(je,[["render",He],["__scopeId","data-v-5ab3e890"]]),Ne="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAADFUlEQVR4nO2Yy04iQRiFeSaw6QtyU5qL4MZo2LDARFiY6CPwAgRWhEQN+CgsCEkb2uiCJ5B5j5qcCtVpaqqraKZhSKb/5AQ0Lr6vPFVUk0jEE0888cQTz2Zc160vl8tfruuSMHl5edkr3W43bNadTqeWCBrXdddh4Y8sQDqdzo9MgJy6QLfbJbGAe6r/gUajQZB6vU5zdXVFU6vVvFSrVZpKpeKlXC7T2LZNUyqVvFxeXtJcXFx4KRaLNIVCgSafz3vJ5XI02WzWy/n5OU0mk6GRCvDwfgEG7xfg4f0CDN4vwMMXfAIM3i/Aw0sFGLxo9WXwotWXwYtWPyeB9wtYlqUWONXqWJalFjjl6lhhBPjVByxAACqrjmj1ZdXJC1Y/qDpKgaDVB2i73Saz2YweY4BTrb6sOqLVz0qq4xcwTVMtwMPf398Tx3HI9/c3WS6X+DinkIfcuJkAeKUAXx2AzedzCs8CiYeHBwp4zOqYYQTYpgXY8/Mz+fz8FEoA7ljVMU2TGIYRLBB06qgkAHaoM9/ywYcW8J/5gBNJ4OenpycKeIgz3+JWXykgO/MBBliRBOSYRJRnvsmt/s4CQdcFgPV6PfL19bUlsVgsKEyUG9cUwOu6Hiygui5gdVutFhkMBuTt7c2TwJWa1eiQ1THCCvDw+DDDPX48HpPhcEglPj4+yOPjoxA+6urouq4WEFWHwU8mEzKdTsnr6yuV6Pf75Pr6egs+6jPf4OClAqLqMHiAv7+/01cEAjc3N6E27j5nvsEJpNNptQC/+qgK4FlQIxG8XwBwqiroGyBE0zSas7MzL6lUiv6O//udBVj37+7uPAm83t7ebp37ouoAHvtjtVrtHcdxSDKZ/ENWKiC65wOy2WyS0Wi0tfKy6kDgb+BXmzABBi8VkN3zAYke43WX6wIqcwgBTdPUAlE8IkIAFYiiQmlun0gFonpExKki2rj+KmgBGxcBOIL3ewn8i3u+scMpJRUolUrrYzwi7nJd0APgU6lU8Je7tm3XIHGsbxdMyWeEqGqA1zStGigQTzzxxBPPfze/AXD61zV6GQOfAAAAAElFTkSuQmCC",Ie="data:image/svg+xml,%3c?xml%20version='1.0'%20encoding='UTF-8'?%3e%3csvg%20width='256px'%20height='255px'%20viewBox='0%200%20256%20255'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3e%3c!--%20Generator:%20Sketch%2052%20(66869)%20-%20http://www.bohemiancoding.com/sketch%20--%3e%3ctitle%3epython%3c/title%3e%3cdesc%3eCreated%20with%20Sketch.%3c/desc%3e%3cdefs%3e%3clinearGradient%20x1='12.9593594%25'%20y1='12.0393928%25'%20x2='79.6388325%25'%20y2='78.2008538%25'%20id='linearGradient-1'%3e%3cstop%20stop-color='%23387EB8'%20offset='0%25'%3e%3c/stop%3e%3cstop%20stop-color='%23366994'%20offset='100%25'%3e%3c/stop%3e%3c/linearGradient%3e%3clinearGradient%20x1='19.127525%25'%20y1='20.5791813%25'%20x2='90.7415328%25'%20y2='88.4290372%25'%20id='linearGradient-2'%3e%3cstop%20stop-color='%23FFE052'%20offset='0%25'%3e%3c/stop%3e%3cstop%20stop-color='%23FFC331'%20offset='100%25'%3e%3c/stop%3e%3c/linearGradient%3e%3c/defs%3e%3cg%20id='Page-1'%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%3e%3cg%20id='python'%20fill-rule='nonzero'%3e%3cpath%20d='M126.915866,0.0722755491%20C62.0835831,0.0722801733%2066.1321288,28.1874648%2066.1321288,28.1874648%20L66.2044043,57.3145115%20L128.072276,57.3145115%20L128.072276,66.0598532%20L41.6307171,66.0598532%20C41.6307171,66.0598532%200.144551098,61.3549438%200.144551098,126.771315%20C0.144546474,192.187673%2036.3546019,189.867871%2036.3546019,189.867871%20L57.9649915,189.867871%20L57.9649915,159.51214%20C57.9649915,159.51214%2056.8001363,123.302089%2093.5968379,123.302089%20L154.95878,123.302089%20C154.95878,123.302089%20189.434218,123.859386%20189.434218,89.9830604%20L189.434218,33.9695088%20C189.434218,33.9695041%20194.668541,0.0722755491%20126.915866,0.0722755491%20Z%20M92.8018069,19.6589497%20C98.9572068,19.6589452%20103.932242,24.6339846%20103.932242,30.7893845%20C103.932246,36.9447844%2098.9572068,41.9198193%2092.8018069,41.9198193%20C86.646407,41.9198239%2081.6713721,36.9447844%2081.6713721,30.7893845%20C81.6713674,24.6339846%2086.646407,19.6589497%2092.8018069,19.6589497%20Z'%20id='Shape'%20fill='url(%23linearGradient-1)'%3e%3c/path%3e%3cpath%20d='M128.757101,254.126271%20C193.589403,254.126271%20189.540839,226.011081%20189.540839,226.011081%20L189.468564,196.884035%20L127.600692,196.884035%20L127.600692,188.138693%20L214.042251,188.138693%20C214.042251,188.138693%20255.528417,192.843589%20255.528417,127.427208%20C255.52844,62.0108566%20219.318366,64.3306589%20219.318366,64.3306589%20L197.707976,64.3306589%20L197.707976,94.6863832%20C197.707976,94.6863832%20198.87285,130.896434%20162.07613,130.896434%20L100.714182,130.896434%20C100.714182,130.896434%2066.238745,130.339138%2066.238745,164.215486%20L66.238745,220.229038%20C66.238745,220.229038%2061.0044225,254.126271%20128.757101,254.126271%20Z%20M162.87116,234.539597%20C156.715759,234.539597%20151.740726,229.564564%20151.740726,223.409162%20C151.740726,217.253759%20156.715759,212.278727%20162.87116,212.278727%20C169.026563,212.278727%20174.001595,217.253759%20174.001595,223.409162%20C174.001618,229.564564%20169.026563,234.539597%20162.87116,234.539597%20Z'%20id='Shape'%20fill='url(%23linearGradient-2)'%3e%3c/path%3e%3c/g%3e%3c/g%3e%3c/svg%3e",Me="data:image/svg+xml,%3csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20128%20128'%3e%3cpath%20fill='%23F0DB4F'%20d='M1.408%201.408h125.184v125.185h-125.184z'/%3e%3cpath%20fill='%23323330'%20d='M116.347%2096.736c-.917-5.711-4.641-10.508-15.672-14.981-3.832-1.761-8.104-3.022-9.377-5.926-.452-1.69-.512-2.642-.226-3.665.821-3.32%204.784-4.355%207.925-3.403%202.023.678%203.938%202.237%205.093%204.724%205.402-3.498%205.391-3.475%209.163-5.879-1.381-2.141-2.118-3.129-3.022-4.045-3.249-3.629-7.676-5.498-14.756-5.355l-3.688.477c-3.534.893-6.902%202.748-8.877%205.235-5.926%206.724-4.236%2018.492%202.975%2023.335%207.104%205.332%2017.54%206.545%2018.873%2011.531%201.297%206.104-4.486%208.08-10.234%207.378-4.236-.881-6.592-3.034-9.139-6.949-4.688%202.713-4.688%202.713-9.508%205.485%201.143%202.499%202.344%203.63%204.26%205.795%209.068%209.198%2031.76%208.746%2035.83-5.176.165-.478%201.261-3.666.38-8.581zm-46.885-37.793h-11.709l-.048%2030.272c0%206.438.333%2012.34-.714%2014.149-1.713%203.558-6.152%203.117-8.175%202.427-2.059-1.012-3.106-2.451-4.319-4.485-.333-.584-.583-1.036-.667-1.071l-9.52%205.83c1.583%203.249%203.915%206.069%206.902%207.901%204.462%202.678%2010.459%203.499%2016.731%202.059%204.082-1.189%207.604-3.652%209.448-7.401%202.666-4.915%202.094-10.864%202.07-17.444.06-10.735.001-21.468.001-32.237z'/%3e%3c/svg%3e",ze="data:image/svg+xml,%3c?xml%20version='1.0'%20encoding='UTF-8'?%3e%3csvg%20width='189px'%20height='256px'%20viewBox='0%200%20189%20256'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3e%3c!--%20Generator:%20Sketch%2052%20(66869)%20-%20http://www.bohemiancoding.com/sketch%20--%3e%3ctitle%3ejava%3c/title%3e%3cdesc%3eCreated%20with%20Sketch.%3c/desc%3e%3cg%20id='Page-1'%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%3e%3cg%20id='java'%3e%3cpath%20d='M60.9480327,197.898746%20C60.9480327,197.898746%2051.20388,203.577614%2067.8826145,205.499268%20C88.0884327,207.809387%2098.4153927,207.478091%20120.682342,203.254583%20C120.682342,203.254583%20126.536531,206.933278%20134.712327,210.119505%20C84.7957094,231.559386%2021.7411855,208.877662%2060.9480327,197.898746'%20id='Path'%20fill='%235382A1'%3e%3c/path%3e%3cpath%20d='M54.8484873,169.921107%20C54.8484873,169.921107%2043.9194763,178.028561%2060.6105818,179.758739%20C82.1950694,181.990338%2099.2408073,182.172861%20128.736491,176.480906%20C128.736491,176.480906%20132.816142,180.625894%20139.231145,182.89262%20C78.878978,200.578731%2011.65752,184.28737%2054.8484873,169.921107'%20id='Path'%20fill='%235382A1'%3e%3c/path%3e%3cpath%20d='M106.269545,122.461747%20C118.568978,136.653063%20103.037989,149.423458%20103.037989,149.423458%20C103.037989,149.423458%20134.268349,133.266405%20119.925655,113.033931%20C106.530022,94.1658991%2096.2573567,84.7911177%20151.869403,52.4680596%20C151.869403,52.4680596%2064.5768327,74.3170664%20106.269545,122.461747'%20id='Path'%20fill='%23E76F00'%3e%3c/path%3e%3cpath%20d='M172.288277,218.592693%20C172.288277,218.592693%20179.499142,224.547068%20164.34684,229.153529%20C135.534305,237.900846%2044.4259963,240.54226%2019.1164909,229.502044%20C10.0183745,225.535446%2027.07992,220.030835%2032.4468327,218.875776%20C38.0439818,217.659416%2041.2425491,217.886021%2041.2425491,217.886021%20C31.12452,210.742837%20-24.1562618,231.912033%2013.1626473,237.974544%20C114.936742,254.515238%20198.687109,230.526238%20172.288277,218.592693'%20id='Path'%20fill='%235382A1'%3e%3c/path%3e%3cpath%20d='M65.6338582,140.93305%20C65.6338582,140.93305%2019.2903709,151.964312%2049.2224727,155.97017%20C61.8607309,157.66591%2087.0547747,157.282268%20110.522389,155.311711%20C129.701422,153.690358%20148.959491,150.243088%20148.959491,150.243088%20C148.959491,150.243088%20142.196727,153.145545%20137.304033,156.493632%20C90.2430327,168.897602%20-0.670090909,163.127128%2025.5026291,150.439386%20C47.6369345,139.716691%2065.6338582,140.93305%2065.6338582,140.93305'%20id='Path'%20fill='%235382A1'%3e%3c/path%3e%3cpath%20d='M148.768429,187.503214%20C196.608109,162.589891%20174.488923,138.648416%20159.050029,141.873903%20C155.265905,142.663228%20153.578651,143.347172%20153.578651,143.347172%20C153.578651,143.347172%20154.983437,141.141746%20157.666549,140.187118%20C188.209637,129.425851%20211.699243,171.926103%20147.806935,188.758833%20C147.806935,188.759522%20148.547127,188.09624%20148.768429,187.503214'%20id='Path'%20fill='%235382A1'%3e%3c/path%3e%3cpath%20d='M119.925655,0.274817278%20C119.925655,0.274817278%20146.420018,26.8356661%2094.796902,67.6787483%20C53.4004037,100.441927%2085.3572106,119.122614%2094.77972,140.466067%20C70.6158982,118.617061%2052.8828873,99.3832953%2064.7795782,81.4822896%20C82.2411167,55.2052121%20130.615495,42.465124%20119.925655,0.274817278'%20id='Path'%20fill='%23E76F00'%3e%3c/path%3e%3cpath%20d='M70.3348037,255.012526%20C116.254931,257.958374%20186.770487,253.378086%20188.44056,231.602778%20C188.44056,231.602778%20185.230309,239.857628%20150.490047,246.413294%20C111.296258,253.805121%2062.9562437,252.942098%2034.2852873,248.204772%20C34.2859745,248.204083%2040.1545963,253.072963%2070.3348037,255.012526'%20id='Path'%20fill='%235382A1'%3e%3c/path%3e%3c/g%3e%3c/g%3e%3c/svg%3e",Fe="/assets/go-DhXD93ZS.svg",Ge="/assets/php-CDNXBikd.svg",De=`curl -X {{{method}}} '{{{url}}}' \\
{{#headers}}
-H '{{{key}}}: {{{value}}}' \\
{{/headers}}
-d '{
  {{#body}}
  "{{{key}}}": {{{value}}}{{^last}},{{/last}}
  {{/body}}
}'
`,Ve=`http {{{method}}} '{{{url}}}' \\
{{#headers}}
  '{{{key}}}:{{{value}}}' \\
{{/headers}}
  --raw='{
  {{#body}}
  "{{{key}}}": {{{value}}}{{^last}},{{/last}}
  {{/body}}
  }'
`,Xe=`wget --quiet \\
  --method={{{method}}} \\
{{#headers}}
  --header='{{{key}}}: {{{value}}}' \\
{{/headers}}
  --body-data='{
  {{#body}}
  "{{{key}}}": {{{value}}}{{^last}},{{/last}}
  {{/body}}
  }' \\
  --output-document=- \\
  '{{{url}}}'
`,We=`import requests

url = "{{{url}}}"

headers = {
{{#headers}}
    "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/headers}}
}

payload = {
{{#body}}
    "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/body}}
}

response = requests.{{{method}}}(url, json=payload, headers=headers)
print(response.text)`,Je=`import httpx

url = "{{{url}}}"

headers = {
{{#headers}}
    "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/headers}}
}

payload = {
{{#body}}
    "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/body}}
}

with httpx.Client(timeout=60.0) as client:
    response = client.{{{method}}}(url, json=payload, headers=headers)
    print(response.text)
`,Ye=`import asyncio

import aiohttp


async def main() -> None:
    url = "{{{url}}}"

    headers = {
{{#headers}}
        "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/headers}}
    }

    payload = {
{{#body}}
        "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/body}}
    }

    async with aiohttp.ClientSession() as session:
        async with session.{{{method}}}(url, json=payload, headers=headers) as response:
            print(await response.text())


asyncio.run(main())
`,Ke=`import json
import urllib.request

url = "{{{url}}}"

headers = {
{{#headers}}
    "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/headers}}
}

payload = {
{{#body}}
    "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/body}}
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(url, data=data, headers=headers, method="{{{methodUpper}}}")
with urllib.request.urlopen(req) as response:
    print(response.read().decode("utf-8"))
`,Qe=`const options = {
  method: "{{{method}}}",
  headers: {
{{#headers}}
    "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/headers}}
  },
  body: JSON.stringify({
{{#body}}
    "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/body}}
  })
};

fetch("{{{url}}}", options)
  .then(response => response.json())
  .then(response => console.log(response))
  .catch(err => console.error(err));`,Ze=`import axios from "axios";

const { data } = await axios({
  method: "{{{method}}}",
  url: "{{{url}}}",
  headers: {
{{#headers}}
    "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/headers}}
  },
  data: {
{{#body}}
    "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/body}}
  }
});

console.log(data);
`,et=`const xhr = new XMLHttpRequest();
xhr.open("{{{methodUpper}}}", "{{{url}}}");
{{#headers}}
xhr.setRequestHeader("{{{key}}}", {{{value}}});
{{/headers}}

xhr.onload = () => {
  console.log(xhr.responseText);
};

xhr.send(JSON.stringify({
{{#body}}
  "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/body}}
}));
`,tt=`JSONObject jsonObject = new JSONObject();
{{#body}}
jsonObject.put("{{{key}}}", {{{value}}});
{{/body}}
MediaType mediaType = "application/json; charset=utf-8".toMediaType();
RequestBody body = jsonObject.toString().toRequestBody(mediaType);
Request request = new Request.Builder()
  .url("{{{url}}}")
  .{{{method}}}(body)
{{#headers}}
  .addHeader("{{{key}}}", {{{value}}})
{{/headers}}
  .build();

OkHttpClient client = new OkHttpClient();
Response response = client.newCall(request).execute();
System.out.print(response.body!!.string())`,nt=`import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

String body = """
{
{{#body}}
  "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/body}}
}
""";

HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("{{{url}}}"))
{{#headers}}
    .header("{{{key}}}", {{{value}}})
{{/headers}}
    .method("{{{methodUpper}}}", HttpRequest.BodyPublishers.ofString(body))
    .build();

HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());
`,at=`package main

import (
	"fmt"
	"strings"
	"net/http"
	"io/ioutil"
)

func main() {

	url := "{{{url}}}"
	method := "{{{method}}}"

	payload := strings.NewReader(\`{
	{{#body}}
	"{{{key}}}": {{{value}}}{{^last}},{{/last}}
	{{/body}}
	}\`)

	client := &http.Client {
	}
	req, err := http.NewRequest(method, url, payload)

	if err != nil {
		fmt.Println(err)
		return
	}
	{{#headers}}
	req.Header.Add("{{{key}}}", {{{value}}})
	{{/headers}}

	res, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer res.Body.Close()

	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(string(body))
}`,rt=`<?php
require_once("vendor/autoload.php");

$client = new \\GuzzleHttp\\Client();

$response = $client->request("{{{method}}}", "{{{url}}}", [
  "body" => '{
{{#body}}
    "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/body}}
  }',
  "headers" => [
{{#headers}}
    "{{{key}}}": {{{value}}}{{^last}},{{/last}}
{{/headers}}
  ],
]);

echo $response->getBody();`,st=`<?php
$curl = curl_init();

curl_setopt_array($curl, [
    CURLOPT_URL => "{{{url}}}",
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_CUSTOMREQUEST => "{{{methodUpper}}}",
    CURLOPT_POSTFIELDS => json_encode([
{{#body}}
        "{{{key}}}" => {{{value}}}{{^last}},{{/last}}
{{/body}}
    ]),
    CURLOPT_HTTPHEADER => [
{{#headers}}
        "{{{key}}}: " . {{{value}}}{{^last}},{{/last}}
{{/headers}}
    ],
]);

$response = curl_exec($curl);
curl_close($curl);
echo $response;
`,G="Shell",Q="Python",Z="JavaScript",ee="Java",te="Go",ne="PHP",Y={Shell:[{key:"curl",label:"cURL",template:De},{key:"httpie",label:"HTTPie",template:Ve},{key:"wget",label:"wget",template:Xe}],Python:[{key:"requests",label:"requests",template:We},{key:"httpx",label:"httpx",template:Je},{key:"aiohttp",label:"aiohttp",template:Ye},{key:"urllib",label:"urllib",template:Ke}],JavaScript:[{key:"fetch",label:"fetch",template:Qe},{key:"axios",label:"axios",template:Ze},{key:"xhr",label:"XHR",template:et}],Java:[{key:"okhttp",label:"OkHttp",template:tt},{key:"httpclient",label:"HttpClient",template:nt}],Go:[{key:"nethttp",label:"net/http",template:at}],PHP:[{key:"guzzle",label:"Guzzle",template:rt},{key:"curl",label:"cURL",template:st}]},ot=[{name:G,icon:Ne},{name:Q,icon:Ie},{name:Z,icon:Me},{name:ee,icon:ze},{name:te,icon:Fe},{name:ne,icon:Ge}],lt="https://platform.acedata.cloud/",it="https://platform.acedata.cloud/favicon.ico",ct=B({name:"ApiCodeDialog",components:{ElDialog:pe,ElButton:ye,ElImage:ge,FontAwesomeIcon:K,CodeSnippet:Oe},props:{visible:{type:Boolean,default:!1},method:{type:String,default:"POST"},path:{type:String,required:!0},body:{type:Object,default:()=>({})},token:{type:String,default:""}},emits:["update:visible"],data(){return{lang:G,variant:"curl",platformIcon:it}},computed:{languages(){return ot},currentVariants(){return Y[this.lang]||[]},url(){const e=de.replace(/\/$/,""),t=this.path.startsWith("/")?this.path:`/${this.path}`;return`${e}${t}`},bearer(){return this.token?this.token:"<YOUR_API_KEY>"},rawHeaders(){const e=[{key:"authorization",value:`Bearer ${this.bearer}`},{key:"content-type",value:"application/json"}];return e[e.length-1].last=!0,e},rawBody(){const e=this.body||{},t=[];for(const[n,a]of Object.entries(e))t.push({key:n,value:a});return t.length>0&&(t[t.length-1].last=!0),t},code(){const e=this.currentVariants.find(r=>r.key===this.variant)||this.currentVariants[0];if(!e)return"";const t=e.template,n=this.rawHeaders.map(r=>({...r})),a=this.rawBody.map(r=>({...r}));let s=String(this.method||"POST").toLowerCase(),o=String(this.method||"POST").toUpperCase(),l=o;const i=r=>JSON.stringify(r);if(this.lang===Q){for(const r of n)r.value=i(r.value);for(const r of a){const c=r.value;c===!0||c===!1?r.value=c?"True":"False":c===null?r.value="None":r.value=i(c)}l=s}else if(this.lang===Z){for(const r of n)r.value=i(r.value);for(const r of a)r.value=i(r.value);l=o}else if(this.lang===ne||this.lang===ee||this.lang===te){for(const r of n)r.value=i(r.value);for(const r of a)r.value=i(r.value);l=o}else if(this.lang===G){for(const r of a)r.value=i(r.value);l=o}return C.render(t,{url:this.url,method:l,methodUpper:o,headers:n,body:a})}},methods:{onSelectLang(e){this.lang=e,this.variant=Y[e][0]?.key||""},onOpenPlatform(){window.open(lt,"_blank","noopener")}}}),pt={class:"intro"},dt={class:"languages mb-2"},ht=["onClick"],ut={class:"name"},ft={key:0,class:"variants mb-2"},gt=["onClick"],yt={key:1,class:"code"},vt={class:"footer"},mt=["src"];function wt(e,t,n,a,s,o){const l=k("el-image"),i=k("code-snippet"),r=k("font-awesome-icon"),c=k("el-button"),h=k("el-dialog");return m(),N(h,{"model-value":e.visible,title:e.$t("common.title.apiCode"),width:"760","close-on-click-modal":!0,class:"api-code-dialog",onClose:t[0]||(t[0]=p=>e.$emit("update:visible",!1))},{footer:U(()=>[S("div",vt,[P(c,{class:"platform-btn",type:"primary",plain:"",onClick:e.onOpenPlatform},{default:U(()=>[S("img",{src:e.platformIcon,class:"platform-icon",alt:""},null,8,mt),le(" "+E(e.$t("common.button.apiPlatform"))+" ",1),P(r,{icon:"fa-solid fa-up-right-from-square",class:"ml-2 ext-icon"})]),_:1},8,["onClick"])])]),default:U(()=>[S("p",pt,E(e.$t("common.message.apiCodeIntro")),1),S("div",dt,[(m(!0),T(X,null,V(e.languages,p=>(m(),T("button",{key:p.name,type:"button",class:I({language:!0,active:e.lang===p.name}),onClick:y=>e.onSelectLang(p.name)},[P(l,{src:p.icon,class:"icon"},null,8,["src"]),S("span",ut,E(p.name),1)],10,ht))),128))]),e.currentVariants.length>1?(m(),T("div",ft,[(m(!0),T(X,null,V(e.currentVariants,p=>(m(),T("button",{key:p.key,type:"button",class:I({variant:!0,active:e.variant===p.key}),onClick:y=>e.variant=p.key},E(p.label),11,gt))),128))])):F("",!0),e.code?(m(),T("div",yt,[(m(),N(i,{key:`${e.lang}-${e.variant}-${e.code.length}`,code:e.code,lang:e.lang},null,8,["code","lang"]))])):F("",!0)]),_:1},8,["model-value","title"])}const Bt=H(ct,[["render",wt],["__scopeId","data-v-9ea1a01e"]]),Ct=B({name:"TopLoading",components:{ElIcon:ue,Loading:he},props:{text:{type:String,default:""},size:{type:Number,default:12},floating:{type:Boolean,default:!0}},computed:{label(){return this.text||this.$t("common.status.loading")}}});function bt(e,t,n,a,s,o){const l=k("loading"),i=k("el-icon");return m(),T("div",{class:I(["top-loading",{floating:e.floating}]),role:"status","aria-live":"polite"},[P(i,{class:"is-loading",size:e.size},{default:U(()=>[P(l)]),_:1},8,["size"]),S("span",null,E(e.label),1)],2)}const kt=H(Ct,[["render",bt],["__scopeId","data-v-763f2217"]]),Tt=120,At=B({name:"ScrollList",components:{TopLoading:kt},props:{loading:{type:Boolean,default:!1},loadingText:{type:String,default:""},floatingLoader:{type:Boolean,default:!0},reachThreshold:{type:Number,default:200}},emits:["reach-top","scroll"],data(){return{scrollEndTimer:0,lastScrollTop:-1,emitsDuringLoad:0}},watch:{loading(e,t){if(e){this.emitsDuringLoad=0;return}t&&this.emitsDuringLoad>0&&(this.emitsDuringLoad=0,this.$emit("reach-top"))}},beforeUnmount(){this.scrollEndTimer&&(window.clearTimeout(this.scrollEndTimer),this.scrollEndTimer=0)},methods:{thresholdPx(e){return Math.max(this.reachThreshold,e.clientHeight||0)},onHandleScroll(){const e=this.$refs.panel;this.$emit("scroll",e);const t=e.scrollTop,n=this.thresholdPx(e),a=this.lastScrollTop<0||t<this.lastScrollTop;this.lastScrollTop=t,a&&t<=n&&this.fireReachTop(),this.scrollEndTimer&&window.clearTimeout(this.scrollEndTimer),this.scrollEndTimer=window.setTimeout(()=>{this.scrollEndTimer=0;const s=this.$refs.panel;s&&s.scrollTop<=this.thresholdPx(s)&&this.fireReachTop()},Tt)},fireReachTop(){this.loading&&(this.emitsDuringLoad+=1),this.$emit("reach-top")},getScrollElement(){return this.$refs.panel}}});function St(e,t,n,a,s,o){const l=k("top-loading");return m(),T("div",{ref:"panel",class:"scroll-list relative",onScroll:t[0]||(t[0]=(...i)=>e.onHandleScroll&&e.onHandleScroll(...i))},[e.loading?(m(),N(l,{key:0,text:e.loadingText,floating:e.floatingLoader},null,8,["text","floating"])):F("",!0),ie(e.$slots,"default",{},void 0,!0)],544)}const Ht=H(At,[["render",St],["__scopeId","data-v-70b67d8a"]]);async function _t(e){const{tasks:t,getTasks:n,loading:a,ignoreLoadingGuard:s,setLoading:o,isBlocked:l,fetch:i,getScrollElement:r,reachThreshold:c=200,_depth:h=0}=e,p=1,y=n?n():t;if(a&&!s||l?.())return;const q=y?.total,$=y?.items?.length||0;if(q!==void 0&&q<=$)return;const d=y?.items?.[0];if(!d?.created_at)return;const b=r?.(),u=b?.scrollHeight||0,f=b?.scrollTop||0,A=$,L=f<=c;o(!0);try{await i(d.created_at),await ce();const w=n?n():t,_=w?.items?.length||0,M=w?.total!==void 0?_<(w.total||0):_>A,v=r?.();if(v){const ae=v.scrollHeight;v.scrollTop=ae-u+f}M&&_>A&&L&&!l?.()&&h<p&&await _t({...e,tasks:w,loading:!1,ignoreLoadingGuard:!0,_depth:h+1})}finally{o(!1)}}export{Bt as A,jt as I,Ht as S,_t as l};
