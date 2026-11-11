// Offline data/control logic only; this is not a browser rendering test.
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const html=fs.readFileSync(process.argv[2],'utf8');
const data=html.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const script=html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
class Element {
 constructor(){this.children=[];this.value='';this.style={};this.events={};this.classList={add(){}};this._text='';}
 set textContent(v){this._text=String(v);this.children=[];}
 get textContent(){return this._text+this.children.map(x=>x.textContent).join(' ');}
 append(...xs){this.children.push(...xs);}
 replaceChildren(...xs){this._text='';this.children=xs;}
 setAttribute(k,v){this[k]=v;}
 addEventListener(k,v){this.events[k]=v;}
}
const ids={};for(const match of html.matchAll(/id="([^"]+)"/g)) ids[match[1]]=new Element();
ids.data.textContent=data;ids.step.value='0';ids.slice.value='0';ids.color.value='energy';
const context=vm.createContext({document:{getElementById:id=>ids[id],createElement:()=>new Element()},console});
vm.runInContext(script,context);
assert.equal(ids.grid.children.length,9);
assert.equal(ids.stepLabel.textContent,'0');
ids.step.value='3';ids.slice.value='2';ids.color.value='charge';ids.step.events.input();ids.grid.children[8].onclick();
assert.equal(ids.grid.children.length,9);assert(ids.nodeTitle.textContent.includes('(2, 2, 2)'));
const D=JSON.parse(data),n=D.snapshots[3].nodes.find(n=>n.xyz.join(',')==='2,2,2');
const fraction=x=>x.den==='1'?x.num:x.num+' / '+x.den;
assert.equal(ids.totalEnergy.textContent,fraction(n.matter.rho_total));
assert.equal(ids.charge.textContent,fraction(n.matter.electric_charge));
ids.color.value='constraint';ids.color.events.input();
assert(ids.constraints.textContent.includes(fraction(n.constraints.H)));
assert.equal(ids.metric.children[0].children.length,3);
console.log(JSON.stringify({kind:'offline JavaScript logic with DOM stubs; not a browser rendering test',nodes:9,selected_node:ids.nodeTitle.textContent,exact_energy:ids.totalEnergy.textContent,exact_charge:ids.charge.textContent,controls:'passed'}));
