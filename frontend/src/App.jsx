import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine
} from 'recharts';

/* ─── CSS embutido ─────────────────────────────────────────────────────────── */
const css = `
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap');

:root {
  --bg:       #F7F6F3;
  --surface:  #FFFFFF;
  --surf2:    #EFEFEB;
  --border:   #E2E0DA;
  --text:     #1A1916;
  --muted:    #8C8880;
  --faint:    #C8C5BE;
  --accent:   #1A6B3C;
  --accent2:  #E8F5EE;
  --warn:     #B45309;
  --warn2:    #FEF3C7;
  --danger:   #B91C1C;
  --danger2:  #FEE2E2;
  --blue:     #1D4ED8;
  --line1:    #1A6B3C;
  --line2:    #B45309;
  --r: 6px;
}

[data-theme=dark] {
  --bg:       #111110;
  --surface:  #1C1C1A;
  --surf2:    #242422;
  --border:   #2E2E2B;
  --text:     #F0EDE8;
  --muted:    #78756E;
  --faint:    #3A3835;
  --accent:   #34D170;
  --accent2:  #0D2B1A;
  --warn:     #F59E0B;
  --warn2:    #2D1F08;
  --danger:   #F87171;
  --danger2:  #2D1010;
  --blue:     #60A5FA;
  --line1:    #34D170;
  --line2:    #F59E0B;
}

*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  background:var(--bg);color:var(--text);
  font-family:'DM Sans',sans-serif;font-size:14px;line-height:1.5;
  -webkit-font-smoothing:antialiased;min-height:100vh;
  transition:background .2s,color .2s;
}

/* HEADER */
.hdr{
  position:sticky;top:0;z-index:100;
  background:var(--bg);border-bottom:1px solid var(--border);
  padding:0 32px;height:52px;
  display:flex;align-items:center;justify-content:space-between;
}
.hdr-logo{display:flex;align-items:center;gap:10px}
.hdr-mark{
  width:28px;height:28px;background:var(--accent);
  border-radius:6px;display:flex;align-items:center;justify-content:center;
}
.hdr-mark svg{width:14px;height:14px;stroke:#fff;fill:none;stroke-width:2;stroke-linecap:round}
.hdr-name{font-size:13px;font-weight:500;letter-spacing:-.01em}
.hdr-name b{color:var(--accent)}
.hdr-sub{font-size:10px;color:var(--muted);letter-spacing:.04em;text-transform:uppercase;margin-top:1px}
.hdr-right{display:flex;align-items:center;gap:8px}
.pill{
  display:flex;align-items:center;gap:5px;
  padding:4px 10px;border:1px solid var(--border);
  border-radius:99px;font-size:11px;color:var(--muted);
  background:var(--surface);font-family:'DM Mono',monospace;
}
.dot{width:5px;height:5px;border-radius:50%;background:var(--accent);animation:blink 2.5s ease infinite}
.dot.off{background:var(--danger);animation:none}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.2}}
.btn-sm{
  height:28px;padding:0 10px;border-radius:99px;
  border:1px solid var(--border);background:var(--surface);
  color:var(--muted);font-family:'DM Sans',sans-serif;
  font-size:11px;cursor:pointer;transition:all .15s;
}
.btn-sm:hover{background:var(--surf2);color:var(--text)}

/* HERO */
.hero{
  padding:40px 32px 28px;border-bottom:1px solid var(--border);
  max-width:1240px;margin:0 auto;width:100%;
}
.hero-tag{
  display:inline-flex;align-items:center;gap:6px;
  font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--accent);font-weight:500;margin-bottom:12px;
}
.hero-tag span{
  width:16px;height:1px;background:var(--accent);display:inline-block;
}
.hero h1{
  font-size:32px;font-weight:300;letter-spacing:-.03em;
  line-height:1.05;margin-bottom:10px;
}
.hero h1 strong{font-weight:500}
.hero p{font-size:13px;color:var(--muted);max-width:420px;line-height:1.7}

/* TABS */
.tabs{
  max-width:1240px;margin:0 auto;width:100%;
  padding:0 32px;border-bottom:1px solid var(--border);
  display:flex;gap:0;overflow-x:auto;scrollbar-width:none;
}
.tabs::-webkit-scrollbar{display:none}
.tab-btn{
  padding:12px 16px;border:none;border-bottom:2px solid transparent;
  background:transparent;color:var(--muted);
  font-family:'DM Sans',sans-serif;font-size:12px;font-weight:400;
  cursor:pointer;white-space:nowrap;transition:all .15s;
  display:flex;align-items:center;gap:6px;
}
.tab-btn:hover{color:var(--text)}
.tab-btn.active{color:var(--text);border-bottom-color:var(--accent);font-weight:500}
.tab-badge{
  width:5px;height:5px;border-radius:50%;
  background:var(--danger);display:inline-block;
}

/* CONTENT */
.content{max-width:1240px;margin:0 auto;width:100%;padding:24px 32px 64px}

/* BANNER */
.banner{
  padding:12px 16px;border-radius:var(--r);
  border:1px solid;margin-bottom:16px;
  display:flex;align-items:flex-start;gap:12px;
}
.banner.danger{border-color:var(--danger);background:var(--danger2)}
.banner.warn{border-color:var(--warn);background:var(--warn2)}
.banner-ico{font-size:14px;margin-top:1px;flex-shrink:0}
.banner-ttl{font-size:12px;font-weight:500;margin-bottom:3px}
.banner.danger .banner-ttl{color:var(--danger)}
.banner.warn .banner-ttl{color:var(--warn)}
.banner-dsc{font-size:11px;color:var(--muted);line-height:1.6}

/* STATS ROW */
.stats{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:var(--r);overflow:hidden;margin-bottom:20px}
.stat{background:var(--surface);padding:16px 18px}
.stat-lbl{font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:8px;font-family:'DM Mono',monospace}
.stat-val{font-size:24px;font-weight:500;letter-spacing:-.03em;line-height:1}
.stat-val.g{color:var(--accent)}
.stat-val.w{color:var(--warn)}
.stat-val.d{color:var(--danger)}
.stat-unit{font-size:10px;color:var(--faint);margin-top:4px;font-family:'DM Mono',monospace}

/* GRID GRÁFICOS */
.chart-grid{display:grid;grid-template-columns:1fr 260px;gap:16px;margin-bottom:16px}
.chart-full{margin-bottom:16px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:18px 20px}
.card-hdr{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:4px}
.card-ttl{font-size:12px;font-weight:500}
.card-sub{font-size:11px;color:var(--muted);margin-bottom:16px}
.chart-wrap{height:210px}

/* NIVEL PANEL */
.nivel{display:flex;flex-direction:column;gap:18px;padding-top:4px}
.n-lbl{font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:5px;font-family:'DM Mono',monospace}
.n-val{font-size:20px;font-weight:500;letter-spacing:-.02em}
.n-bar{height:2px;background:var(--surf2);border-radius:99px;margin-top:8px;overflow:hidden}
.n-fill{height:100%;border-radius:99px;transition:width 1.2s cubic-bezier(.4,0,.2,1)}
.n-fill.g{background:var(--accent)}
.n-fill.w{background:var(--warn)}
.n-fill.d{background:var(--danger)}
.n-status{font-size:12px;font-weight:500;margin-top:3px}

/* PREVISÃO */
.prev-card{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r);padding:18px 20px;margin-bottom:16px;
}
.prev-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:12px}
.prev-item{}
.prev-lbl{font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-family:'DM Mono',monospace;margin-bottom:6px}
.prev-val{font-size:18px;font-weight:500;letter-spacing:-.02em}
.prev-desc{font-size:11px;color:var(--muted);margin-top:3px;line-height:1.5}

/* MAPA SECTION */
.map-section{margin-top:8px}
.map-title-row{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.map-title{font-size:14px;font-weight:500}
.map-sub{font-size:12px;color:var(--muted)}
.map-wrap{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r);overflow:hidden;height:380px;position:relative;
}
#mapa-leaflet{width:100%;height:100%}

/* FILTRO */
.filtro-row{display:flex;align-items:center;gap:10px;margin-bottom:16px}
.filtro-lbl{font-size:11px;color:var(--muted)}
.filtro-sel{
  background:var(--surface);border:1px solid var(--border);
  color:var(--text);padding:5px 12px;border-radius:99px;
  font-family:'DM Sans',sans-serif;font-size:11px;
  cursor:pointer;outline:none;
}

/* ESTADO */
.state{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:320px;gap:12px;color:var(--muted)}
.spinner{width:22px;height:22px;border-radius:50%;border:2px solid var(--border);border-top-color:var(--accent);animation:spin .6s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}

/* FOOTER */
.footer{border-top:1px solid var(--border);padding:14px 32px;text-align:center;font-size:11px;color:var(--faint);font-family:'DM Mono',monospace}

@media(max-width:900px){
  .stats{grid-template-columns:repeat(3,1fr)}
  .chart-grid{grid-template-columns:1fr}
  .prev-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:600px){
  .hero{padding:28px 20px 20px}
  .tabs{padding:0 20px}
  .content{padding:16px 20px 48px}
  .stats{grid-template-columns:1fr 1fr}
  .hdr{padding:0 20px}
}
`;

/* ─── Constantes ──────────────────────────────────────────────────────────── */
const ALERTAS = {
  "Manaus": { tipo: "danger", titulo: "Alerta de enchente — Manaus", desc: "Zona Sul com risco elevado. Nível acima da cota de atenção desde 24/04/2026." }
};

const CONFIG_ESTACOES = {
  "Manaus":      { lat: -3.10, lon: -60.02, cota_alerta: 29.00, cota_max: 29.97 },
  "Itacoatiara": { lat: -3.14, lon: -58.44, cota_alerta: 14.00, cota_max: 16.83 },
  "Manacapuru":  { lat: -3.31, lon: -60.61, cota_alerta: 21.00, cota_max: 23.50 },
  "Parintins":   { lat: -2.63, lon: -56.74, cota_alerta: 11.50, cota_max: 13.80 },
  "Óbidos":      { lat: -1.92, lon: -55.52, cota_alerta:  9.00, cota_max: 11.20 },
  "Tefé":        { lat: -3.37, lon: -64.72, cota_alerta: 14.50, cota_max: 17.50 },
  "Santarém":    { lat: -2.44, lon: -54.70, cota_alerta:  8.50, cota_max: 10.50 },
  "Tabatinga":   { lat: -4.25, lon: -69.94, cota_alerta: 11.00, cota_max: 13.50 },
};

const PERIODOS = [
  { label: 'Todos os dados', value: 0 },
  { label: 'Últimos 30 dias', value: 30 },
  { label: 'Últimos 60 dias', value: 60 },
  { label: 'Últimos 90 dias', value: 90 },
];

const fmtData = s => { if (!s) return ''; const [,m,d] = s.split('-'); return `${d}/${m}`; };

function classificar(cota, cfg) {
  if (!cfg) return { cls: 'g', txt: 'Normal', pct: 0 };
  const pct = Math.min((cota / cfg.cota_max) * 100, 100);
  if (cota >= cfg.cota_alerta * 1.2) return { cls: 'd', txt: 'Emergência', pct };
  if (cota >= cfg.cota_alerta)       return { cls: 'd', txt: 'Alerta',     pct };
  if (cota >= cfg.cota_alerta * 0.7) return { cls: 'w', txt: 'Atenção',    pct };
  return { cls: 'g', txt: 'Normal', pct };
}

/* Estima pico: pega máximo dos próximos 15 dias da tendência */
function estimarPico(lista) {
  if (!lista || lista.length < 7) return null;
  const recente = lista.slice(-14);
  const diffs = recente.slice(1).map((d, i) => (d.cota_m ?? 0) - (recente[i].cota_m ?? 0));
  const tendencia = diffs.reduce((a, b) => a + b, 0) / diffs.length;
  const ult = lista[lista.length - 1];
  const cotaAtual = ult?.cota_m ?? 0;
  if (tendencia <= 0) return { data: 'Estável', cota: cotaAtual, desc: 'Rio em queda ou estável' };
  const diasPico = Math.round((0 - tendencia * 14) / tendencia) + 14;
  const cotaPico = cotaAtual + tendencia * Math.min(diasPico, 30);
  const dataPico = new Date();
  dataPico.setDate(dataPico.getDate() + Math.min(diasPico, 30));
  return {
    data: dataPico.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' }),
    cota: Math.min(cotaPico, 35).toFixed(2),
    desc: `+${tendencia.toFixed(3)}m/dia tendência`,
    tendencia
  };
}

/* ─── Tooltip ─────────────────────────────────────────────────────────────── */
const Tip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background:'var(--surface)', border:'1px solid var(--border)', borderRadius:6, padding:'8px 12px', fontSize:11, boxShadow:'0 4px 20px rgba(0,0,0,.12)' }}>
      <p style={{ color:'var(--muted)', marginBottom:4, fontFamily:'DM Mono,monospace' }}>{label}</p>
      {payload.map((p, i) => <p key={i} style={{ color:p.color, fontWeight:500 }}>{p.name}: {(+p.value).toFixed(2)}</p>)}
    </div>
  );
};

/* ─── App ─────────────────────────────────────────────────────────────────── */
export default function App() {
  const [dados, setDados]       = useState({});
  const [estacoes, setEstacoes] = useState([]);
  const [cidade, setCidade]     = useState('');
  const [periodo, setPeriodo]   = useState(0);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState(null);
  const [tema, setTema]         = useState(() => localStorage.getItem('tema') || 'light');
  const mapaRef = useRef(null);
  const mapaInst = useRef(null);
  const leafletRef = useRef(null);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', tema);
    localStorage.setItem('tema', tema);
  }, [tema]);

  const carregar = async (est = cidade, dias = periodo) => {
    try {
      setLoading(true); setError(null);
      const [rE, rD] = await Promise.all([
        axios.get('/api/estacoes'),
        axios.get('/api/dados', { params: { ...(est && { estacao: est }), ...(dias > 0 && { dias }) } })
      ]);
      const lista = rE.data?.estacoes || [];
      setEstacoes(lista);
      setDados(rD.data);
      if (!est && lista.length) setCidade(lista[0]);
    } catch (e) { setError(e.message); }
    finally { setLoading(false); }
  };

  useEffect(() => { carregar('', 0); }, []);
  useEffect(() => { if (cidade) carregar(cidade, periodo); }, [cidade, periodo]);

  /* ── Mapa Leaflet ── */
  useEffect(() => {
    if (!mapaRef.current) return;
    if (mapaInst.current) return;

    // Carrega Leaflet dinamicamente se não estiver
    const initMap = () => {
      const L = window.L;
      if (!L) return;
      const map = L.map('mapa-leaflet', { zoomControl: true, scrollWheelZoom: false })
        .setView([-3.5, -62], 5);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png', {
        attribution: '© CartoDB', maxZoom: 12
      }).addTo(map);

      Object.entries(CONFIG_ESTACOES).forEach(([nome, cfg]) => {
        const info = dados[nome] || {};
        const lista = info.dados || [];
        const ult = lista[lista.length - 1] || {};
        const cota = ult.cota_m ?? 0;
        const { cls } = classificar(cota, cfg);
        const cor = cls === 'g' ? '#1A6B3C' : cls === 'w' ? '#B45309' : '#B91C1C';

        const icon = L.divIcon({
          className: '',
          html: `<div style="width:12px;height:12px;border-radius:50%;background:${cor};border:2px solid white;box-shadow:0 1px 4px rgba(0,0,0,.3)"></div>`,
          iconSize: [12, 12], iconAnchor: [6, 6]
        });

        L.marker([cfg.lat, cfg.lon], { icon })
          .addTo(map)
          .bindPopup(`<b>${nome}</b><br/>Cota: ${cota.toFixed(2)}m<br/>Status: ${cls === 'g' ? 'Normal' : cls === 'w' ? 'Atenção' : 'Alerta'}`, { maxWidth: 160 })
          .on('click', () => setCidade(nome));
      });

      mapaInst.current = map;
    };

    if (window.L) { initMap(); return; }
    const link = document.createElement('link');
    link.rel = 'stylesheet'; link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    document.head.appendChild(link);
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    script.onload = initMap;
    document.head.appendChild(script);
  }, [mapaRef.current, Object.keys(dados).length]);

  /* Derivados */
  const info   = dados[cidade] || {};
  const lista  = info.dados    || [];
  const ult    = lista[lista.length - 1] || {};
  const cota   = ult.cota_m ?? 0;
  const cfg    = CONFIG_ESTACOES[cidade];
  const { cls, txt: stTxt, pct } = classificar(cota, cfg);
  const stColor = cls === 'g' ? 'var(--accent)' : cls === 'w' ? 'var(--warn)' : 'var(--danger)';
  const al     = ALERTAS[cidade];
  const pico   = estimarPico(lista);
  const fonteLabel = { 'sace': 'SACE/SGB', 'open-meteo': 'Open-Meteo', 'fallback': 'Cache local' }[info.fonte] || info.fonte || '—';

  if (loading && !estacoes.length) return (
    <><style>{css}</style>
    <div className="state" style={{ minHeight:'100vh' }}>
      <div className="spinner" /><span style={{ fontSize:12 }}>Carregando…</span>
    </div></>
  );

  if (error && !estacoes.length) return (
    <><style>{css}</style>
    <div className="state" style={{ minHeight:'100vh' }}>
      <div style={{ background:'var(--surface)', border:'1px solid var(--border)', borderRadius:8, padding:24, maxWidth:380 }}>
        <p style={{ fontWeight:500, color:'var(--danger)', marginBottom:8 }}>Backend offline</p>
        <p style={{ fontSize:12, color:'var(--muted)', lineHeight:1.7 }}>
          Rode o servidor Python:<br/>
          <code style={{ display:'block', marginTop:8, fontSize:11, fontFamily:'DM Mono,monospace', background:'var(--surf2)', padding:'6px 10px', borderRadius:4 }}>
            python -m uvicorn backend.server:app --port 5000 --reload
          </code>
        </p>
        <button className="btn-sm" style={{ marginTop:14 }} onClick={() => carregar('', 0)}>Tentar novamente</button>
      </div>
    </div></>
  );

  return (
    <>
      <style>{css}</style>

      {/* HEADER */}
      <header className="hdr">
        <div className="hdr-logo">
          <div className="hdr-mark">
            <svg viewBox="0 0 14 14"><path d="M1 8 Q3.5 4 7 8 Q10.5 12 13 8"/></svg>
          </div>
          <div>
            <div className="hdr-name">Rio <b>Amazonas</b></div>
            <div className="hdr-sub">Monitor Fluviométrico</div>
          </div>
        </div>
        <div className="hdr-right">
          <div className="pill">
            <span className={`dot${error ? ' off' : ''}`} />
            <span>{error ? 'Offline' : 'Ao vivo'}</span>
          </div>
          <button className="btn-sm" onClick={() => setTema(t => t === 'dark' ? 'light' : 'dark')}>
            {tema === 'dark' ? '☀ Claro' : '◐ Escuro'}
          </button>
        </div>
      </header>

      {/* HERO */}
      <section className="hero">
        <div className="hero-tag"><span/>Monitoramento · Amazonas · 2026</div>
        <h1>Nível do<br/><strong>Rio Amazonas</strong></h1>
        <p>Cotas reais via SACE/SGB em {estacoes.length} estações fluviométricas da bacia amazônica.</p>
      </section>

      {/* TABS */}
      <nav className="tabs">
        {estacoes.map(c => (
          <button key={c} className={`tab-btn${c === cidade ? ' active' : ''}`} onClick={() => setCidade(c)}>
            {c}
            {ALERTAS[c] && <span className="tab-badge"/>}
          </button>
        ))}
      </nav>

      {/* CONTEÚDO */}
      <main className="content">

        {/* FILTRO + STATUS */}
        <div className="filtro-row">
          <span className="filtro-lbl">Período:</span>
          <select className="filtro-sel" value={periodo} onChange={e => setPeriodo(Number(e.target.value))}>
            {PERIODOS.map(p => <option key={p.value} value={p.value}>{p.label}</option>)}
          </select>
          {loading && <div className="spinner" style={{ width:16, height:16 }}/>}
        </div>

        {/* BANNER ALERTA */}
        {al && (
          <div className={`banner ${al.tipo}`}>
            <div className="banner-ico">{al.tipo === 'danger' ? '⚠' : '!'}</div>
            <div>
              <div className="banner-ttl">{al.titulo}</div>
              <div className="banner-dsc">{al.desc}</div>
            </div>
          </div>
        )}

        {!loading && lista.length === 0
          ? <div className="state"><span>Sem dados para <strong>{cidade}</strong>.</span></div>
          : <>
            {/* STATS */}
            <div className="stats">
              <div className="stat">
                <div className="stat-lbl">Cota Atual</div>
                <div className={`stat-val ${cls}`}>{cota.toFixed(2)}</div>
                <div className="stat-unit">metros</div>
              </div>
              <div className="stat">
                <div className="stat-lbl">Cota de Alerta</div>
                <div className="stat-val">{cfg?.cota_alerta?.toFixed(2) ?? '—'}</div>
                <div className="stat-unit">metros</div>
              </div>
              <div className="stat">
                <div className="stat-lbl">% do Máximo</div>
                <div className={`stat-val ${cls}`}>{pct.toFixed(0)}%</div>
                <div className="stat-unit">histórico</div>
              </div>
              <div className="stat">
                <div className="stat-lbl">Registros</div>
                <div className="stat-val">{lista.length}</div>
                <div className="stat-unit">dias</div>
              </div>
              <div className="stat">
                <div className="stat-lbl">Fonte</div>
                <div className="stat-val" style={{ fontSize:13, paddingTop:4 }}>{fonteLabel}</div>
                <div className="stat-unit">{info.fonte === 'sace' ? 'dados reais' : 'estimativa'}</div>
              </div>
            </div>

            {/* GRÁFICOS */}
            <div className="chart-grid">
              {/* Cota histórico */}
              <div className="card">
                <div className="card-hdr">
                  <div className="card-ttl">Cota hídrica</div>
                </div>
                <div className="card-sub">metros — {cidade}</div>
                <div className="chart-wrap">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={lista} margin={{ top:4, right:8, left:0, bottom:0 }}>
                      <CartesianGrid strokeDasharray="2 4" stroke="var(--border)" vertical={false}/>
                      <XAxis dataKey="data" tickFormatter={fmtData} tick={{ fontSize:10, fill:'var(--muted)', fontFamily:'DM Mono,monospace' }} axisLine={false} tickLine={false} interval="preserveStartEnd"/>
                      <YAxis tick={{ fontSize:10, fill:'var(--muted)', fontFamily:'DM Mono,monospace' }} axisLine={false} tickLine={false} width={38} domain={['auto','auto']}/>
                      <Tooltip content={<Tip/>}/>
                      {cfg && <ReferenceLine y={cfg.cota_alerta} stroke="var(--warn)" strokeDasharray="3 3" strokeWidth={1.5} label={{ value:'Alerta', position:'insideTopRight', fontSize:9, fill:'var(--warn)' }}/>}
                      {cfg && <ReferenceLine y={cfg.cota_max} stroke="var(--danger)" strokeDasharray="3 3" strokeWidth={1} label={{ value:'Máx hist.', position:'insideTopRight', fontSize:9, fill:'var(--danger)' }}/>}
                      <Line type="monotone" dataKey="cota_m" name="Cota (m)" stroke="var(--line1)" strokeWidth={1.5} dot={false} activeDot={{ r:4, strokeWidth:0 }}/>
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Painel nível + previsão */}
              <div style={{ display:'flex', flexDirection:'column', gap:16 }}>
                <div className="card" style={{ flex:1 }}>
                  <div className="card-ttl">Nível hídrico</div>
                  <div className="card-sub">status atual</div>
                  <div className="nivel">
                    <div>
                      <div className="n-lbl">Cota</div>
                      <div className="n-val">{cota.toFixed(2)} m</div>
                      <div className="n-bar"><div className={`n-fill ${cls}`} style={{ width:`${pct.toFixed(1)}%` }}/></div>
                    </div>
                    <div>
                      <div className="n-lbl">Alerta em</div>
                      <div className="n-val">{cfg ? (cfg.cota_alerta - cota).toFixed(2) : '—'} m</div>
                      <div className="n-bar">
                        <div className="n-fill g" style={{ width:`${Math.min(((cota/cfg?.cota_alerta||1)*100), 100).toFixed(1)}%` }}/>
                      </div>
                    </div>
                    <div>
                      <div className="n-lbl">Status</div>
                      <div className="n-status" style={{ color: stColor }}>{stTxt}</div>
                    </div>
                  </div>
                </div>

                {pico && (
                  <div className="card">
                    <div className="card-ttl">Previsão de pico</div>
                    <div className="card-sub">estimativa por tendência</div>
                    <div style={{ display:'flex', flexDirection:'column', gap:10 }}>
                      <div>
                        <div className="n-lbl">Data estimada</div>
                        <div className="n-val" style={{ fontSize:16 }}>{pico.data}</div>
                      </div>
                      <div>
                        <div className="n-lbl">Cota estimada</div>
                        <div className="n-val" style={{ fontSize:16 }}>{pico.cota} m</div>
                      </div>
                      <div className="n-lbl" style={{ marginTop:2 }}>{pico.desc}</div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* MAPA */}
            <div className="map-section">
              <div className="map-title-row">
                <div className="map-title">Estações monitoradas</div>
                <div className="map-sub">Clique em um ponto para selecionar a estação</div>
              </div>
              <div className="map-wrap">
                <div id="mapa-leaflet" ref={mapaRef}/>
              </div>
            </div>
          </>
        }
      </main>

      <footer className="footer">
        Rio Amazonas · Dados via SACE/SGB · {new Date().toLocaleDateString('pt-BR', { day:'2-digit', month:'long', year:'numeric' })}
      </footer>
    </>
  );
}
