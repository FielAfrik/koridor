// Régénère site/africa.json (contours des pays africains pour la carte de l'accueil).
// Usage : npm i world-atlas@2 topojson-client topojson-simplify d3-geo i18n-iso-countries
//         node scripts/carte/make.mjs site/countries.json site/africa.json
// Données : Natural Earth via world-atlas (domaine public).
import fs from 'fs';
import {feature} from 'topojson-client';
import {geoMercator, geoPath} from 'd3-geo';
import countries from 'i18n-iso-countries';
const ours = JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const topo = JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-50m.json','utf8'));
import {presimplify, simplify, quantile} from 'topojson-simplify';
const ps=presimplify(topo); const st=simplify(ps, quantile(ps, 0.12));
const fc = feature(st, st.objects.countries);
const want = new Set([...Object.keys(ours),'EH']);
const feats = fc.features.filter(f=>{const a=countries.numericToAlpha2(f.id); if(a){f.properties.a2=a;} return a && want.has(a);});
const missing=[...want].filter(a=>!feats.find(f=>f.properties.a2===a));
const W=600,H=640;
const proj=geoMercator().fitExtent([[8,8],[W-8,H-8]],{type:'FeatureCollection',features:feats.filter(f=>!['CV','MU','SC'].includes(f.properties.a2))});
const path=geoPath(proj).digits(1);
const out={viewBox:`0 0 ${W} ${H}`,paths:{},centroids:{}};
for(const f of feats){const d=path(f); if(!d) continue; out.paths[f.properties.a2]=d; const c=path.centroid(f); out.centroids[f.properties.a2]=c.map(v=>Math.round(v));}
fs.writeFileSync(process.argv[3],JSON.stringify(out));
console.log('features',feats.length,'missing',missing, 'size',fs.statSync(process.argv[3]).size, 'nopath', Object.keys(ours).filter(k=>!out.paths[k]));
