import { useState } from "react";

const concepts = [
  {
    id: "structure", label: "Market Structure", icon: "📊", color: "#00e5ff",
    description: "Identify the trend direction using swing highs and lows.",
    rules: ["Higher Highs + Higher Lows = Uptrend (Bullish)", "Lower Highs + Lower Lows = Downtrend (Bearish)", "BOS (Break of Structure) = trend continuation", "CHoCH (Change of Character) = potential reversal"],
  },
  {
    id: "liquidity", label: "Liquidity", icon: "💧", color: "#ff6b35",
    description: "Find where stop losses cluster — smart money targets these.",
    rules: ["Buy-side liquidity = above swing highs", "Sell-side liquidity = below swing lows", "Equal highs/lows = high probability liquidity zones", "Price sweeps liquidity before reversing"],
  },
  {
    id: "orderblocks", label: "Order Blocks", icon: "🧱", color: "#a78bfa",
    description: "Last opposing candle before a strong institutional move.",
    rules: ["Bullish OB = last bearish candle before rally", "Bearish OB = last bullish candle before drop", "Price returns to OBs to fill institutional orders", "Valid OB should have a strong impulse away from it"],
  },
  {
    id: "fvg", label: "Fair Value Gap", icon: "⚡", color: "#34d399",
    description: "3-candle imbalance where price moves too fast, leaving a gap.",
    rules: ["Candle 1 high to Candle 3 low = Bullish FVG", "Candle 1 low to Candle 3 high = Bearish FVG", "Price often returns to fill the gap", "Unfilled FVGs act as magnets for price"],
  },
  {
    id: "premium", label: "Premium & Discount", icon: "📐", color: "#fbbf24",
    description: "Use Fibonacci 50% to find optimal buy/sell zones.",
    rules: ["Above 50% of the range = Premium (sell zone)", "Below 50% of the range = Discount (buy zone)", "Institutions BUY in discount, SELL in premium", "OTE entry: 62%–79% Fibonacci retracement"],
  },
  {
    id: "killzones", label: "Kill Zones", icon: "🕐", color: "#f87171",
    description: "High-probability trading time windows for institutional activity.",
    rules: ["Asian: 8PM – 11PM EST (range builder)", "London: 2AM – 5AM EST (EUR/GBP best)", "New York: 7AM – 10AM EST (all majors)", "Avoid trading outside these windows"],
  },
  {
    id: "amd", label: "Power of 3 (AMD)", icon: "🔄", color: "#60a5fa",
    description: "Accumulation → Manipulation → Distribution",
    rules: ["Accumulation: price consolidates in a range", "Manipulation: false breakout / stop hunt", "Distribution: true directional move begins", "Applies to daily, weekly, monthly cycles"],
  },
  {
    id: "risk", label: "Risk Management", icon: "🛡️", color: "#4ade80",
    description: "Protect your capital above all else.",
    rules: ["Risk max 0.5%–1% per trade", "Minimum 1:2 Risk:Reward ratio", "Stop loss below/above Order Block", "Max 2–3% daily loss limit then stop"],
  },
];

const checklist = [
  "HTF trend confirmed (Daily/Weekly)",
  "Daily bias set (Bullish or Bearish)",
  "Price in Premium or Discount zone",
  "Liquidity level identified",
  "Inside a Kill Zone session",
  "Liquidity swept (stop hunt occurred)",
  "CHoCH or BOS on lower timeframe",
  "Price at Order Block or FVG",
  "Confirmation candle formed",
  "SL placed below OB, TP at liquidity",
  "Risk = 1% max of account",
];

const biasQuestions = [
  { q: "Is HTF (Daily/Weekly) trending up?", bull: true },
  { q: "Is price in a Discount zone (below 50% fib)?", bull: true },
  { q: "Has sell-side liquidity been swept?", bull: true },
  { q: "Is there a CHoCH on 15M/5M chart?", bull: true },
  { q: "Is there a Bullish Order Block nearby?", bull: true },
];

const patterns = [
  {
    id: "bullish_ob",
    name: "Bullish Order Block",
    type: "bullish",
    color: "#34d399",
    tag: "REVERSAL",
    description: "Last bearish candle before a strong bullish impulse. Price returns here to fill institutional buy orders.",
    howToTrade: "Wait for price to return to the OB zone, look for CHoCH on LTF, enter long with SL below the OB.",
    timeframes: ["15M", "1H", "4H"],
    render: (c) => (
      <svg viewBox="0 0 200 120" style={{ width: "100%", height: 120 }}>
        <defs>
          <linearGradient id="bg1" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#0d2b1a" />
            <stop offset="100%" stopColor="#080c14" />
          </linearGradient>
        </defs>
        <rect width="200" height="120" fill="url(#bg1)" rx="8" />
        {/* Grid lines */}
        {[30,60,90].map(y => <line key={y} x1="10" y1={y} x2="190" y2={y} stroke="#1e293b" strokeWidth="0.5" />)}
        {/* Bearish candles before OB */}
        {[[20,20,45,35],[35,25,50,38],[50,30,55,42]].map(([x,top,bot,body],i) => (
          <g key={i}>
            <line x1={x+5} y1={top} x2={x+5} y2={bot} stroke="#f87171" strokeWidth="1.5" />
            <rect x={x} y={Math.min(body-8,top+2)} width="10" height="10" fill="#f87171" rx="1" />
          </g>
        ))}
        {/* OB candle - highlighted */}
        <rect x="62" y="35" width="16" height="22" fill="#22c55e30" stroke="#34d399" strokeWidth="1.5" rx="2" />
        <line x1="70" y1="28" x2="70" y2="60" stroke="#f87171" strokeWidth="1.5" />
        <rect x="62" y="38" width="16" height="16" fill="#f87171" rx="1" />
        <text x="70" y="75" textAnchor="middle" fill="#34d399" fontSize="7" fontWeight="bold">OB ZONE</text>
        {/* Strong bullish impulse */}
        {[[82,55,20,18],[97,35,10,25],[112,18,5,28],[127,12,3,25]].map(([x,top,wick,body],i) => (
          <g key={i}>
            <line x1={x+5} y1={top-wick} x2={x+5} y2={top+body+4} stroke="#34d399" strokeWidth="1.5" />
            <rect x={x} y={top} width="10" height={body} fill="#34d399" rx="1" />
          </g>
        ))}
        {/* Return to OB */}
        <path d="M 145 18 Q 155 50 155 57" stroke="#fbbf24" strokeWidth="1.5" strokeDasharray="3,2" fill="none" />
        <circle cx="155" cy="58" r="4" fill="#fbbf2440" stroke="#fbbf24" strokeWidth="1.5" />
        <text x="158" y="50" fill="#fbbf24" fontSize="7">Return</text>
        {/* OB zone shading */}
        <rect x="62" y="35" width="95" height="22" fill="#34d39908" stroke="none" />
        <line x1="62" y1="35" x2="160" y2="35" stroke="#34d399" strokeWidth="0.8" strokeDasharray="4,3" />
        <line x1="62" y1="57" x2="160" y2="57" stroke="#34d399" strokeWidth="0.8" strokeDasharray="4,3" />
      </svg>
    ),
  },
  {
    id: "bearish_ob",
    name: "Bearish Order Block",
    type: "bearish",
    color: "#f87171",
    tag: "REVERSAL",
    description: "Last bullish candle before a strong bearish impulse. Price returns here to fill institutional sell orders.",
    howToTrade: "Wait for price to return to the OB zone, look for bearish CHoCH on LTF, enter short with SL above the OB.",
    timeframes: ["15M", "1H", "4H"],
    render: () => (
      <svg viewBox="0 0 200 120" style={{ width: "100%", height: 120 }}>
        <rect width="200" height="120" fill="#080c14" rx="8" />
        {[30,60,90].map(y => <line key={y} x1="10" y1={y} x2="190" y2={y} stroke="#1e293b" strokeWidth="0.5" />)}
        {/* Bullish candles */}
        {[[20,55,75,12],[35,50,72,14],[50,45,68,15]].map(([x,top,bot,body],i) => (
          <g key={i}>
            <line x1={x+5} y1={top} x2={x+5} y2={bot} stroke="#34d399" strokeWidth="1.5" />
            <rect x={x} y={top+4} width="10" height={body} fill="#34d399" rx="1" />
          </g>
        ))}
        {/* OB candle */}
        <rect x="62" y="38" width="16" height="20" fill="#ef444420" stroke="#f87171" strokeWidth="1.5" rx="2" />
        <line x1="70" y1="32" x2="70" y2="62" stroke="#34d399" strokeWidth="1.5" />
        <rect x="62" y="40" width="16" height="14" fill="#34d399" rx="1" />
        <text x="70" y="75" textAnchor="middle" fill="#f87171" fontSize="7" fontWeight="bold">OB ZONE</text>
        {/* Bearish impulse */}
        {[[82,35,10,18],[97,52,5,20],[112,70,4,18],[127,85,3,15]].map(([x,top,wick,body],i) => (
          <g key={i}>
            <line x1={x+5} y1={top-wick} x2={x+5} y2={top+body+4} stroke="#f87171" strokeWidth="1.5" />
            <rect x={x} y={top} width="10" height={body} fill="#f87171" rx="1" />
          </g>
        ))}
        {/* Return arrow */}
        <path d="M 145 88 Q 155 60 155 58" stroke="#fbbf24" strokeWidth="1.5" strokeDasharray="3,2" fill="none" />
        <circle cx="155" cy="57" r="4" fill="#fbbf2440" stroke="#fbbf24" strokeWidth="1.5" />
        <text x="158" y="72" fill="#fbbf24" fontSize="7">Return</text>
        <rect x="62" y="38" width="95" height="20" fill="#f8717108" />
        <line x1="62" y1="38" x2="160" y2="38" stroke="#f87171" strokeWidth="0.8" strokeDasharray="4,3" />
        <line x1="62" y1="58" x2="160" y2="58" stroke="#f87171" strokeWidth="0.8" strokeDasharray="4,3" />
      </svg>
    ),
  },
  {
    id: "fvg_bull",
    name: "Bullish Fair Value Gap",
    type: "bullish",
    color: "#34d399",
    tag: "IMBALANCE",
    description: "3-candle pattern where a strong bullish candle leaves a gap between candle 1 high and candle 3 low.",
    howToTrade: "Mark the gap between C1 high and C3 low. Enter long when price retraces into the gap. SL below the gap.",
    timeframes: ["5M", "15M", "1H"],
    render: () => (
      <svg viewBox="0 0 200 120" style={{ width: "100%", height: 120 }}>
        <rect width="200" height="120" fill="#080c14" rx="8" />
        {[30,60,90].map(y => <line key={y} x1="10" y1={y} x2="190" y2={y} stroke="#1e293b" strokeWidth="0.5" />)}
        {/* C1 */}
        <line x1="45" y1="55" x2="45" y2="90" stroke="#f87171" strokeWidth="1.5" />
        <rect x="38" y="62" width="14" height="20" fill="#f87171" rx="1" />
        <text x="45" y="105" textAnchor="middle" fill="#64748b" fontSize="8">C1</text>
        {/* C2 - big bullish */}
        <line x1="80" y1="18" x2="80" y2="88" stroke="#34d399" strokeWidth="1.5" />
        <rect x="73" y="22" width="14" height="62" fill="#34d399" rx="1" />
        <text x="80" y="105" textAnchor="middle" fill="#34d399" fontSize="8" fontWeight="bold">C2</text>
        {/* C3 */}
        <line x1="115" y1="12" x2="115" y2="45" stroke="#34d399" strokeWidth="1.5" />
        <rect x="108" y="15" width="14" height="22" fill="#34d399" rx="1" />
        <text x="115" y="105" textAnchor="middle" fill="#64748b" fontSize="8">C3</text>
        {/* FVG zone */}
        <rect x="62" y="38" width="35" height="20" fill="#34d39920" stroke="#34d399" strokeWidth="1" rx="2" strokeDasharray="3,2" />
        <text x="79" y="52" textAnchor="middle" fill="#34d399" fontSize="7" fontWeight="bold">FVG</text>
        {/* Lines showing gap */}
        <line x1="38" y1="62" x2="108" y2="62" stroke="#fbbf24" strokeWidth="0.8" strokeDasharray="3,2" />
        <text x="160" y="65" fill="#fbbf24" fontSize="7">C1 High</text>
        <line x1="108" y1="38" x2="38" y2="38" stroke="#60a5fa" strokeWidth="0.8" strokeDasharray="3,2" />
        <text x="145" y="41" fill="#60a5fa" fontSize="7">C3 Low</text>
        {/* Price return */}
        <path d="M 130 18 Q 150 45 150 50" stroke="#fbbf24" strokeWidth="1.5" strokeDasharray="3,2" fill="none" />
        <circle cx="150" cy="50" r="3" fill="#fbbf2440" stroke="#fbbf24" strokeWidth="1.5" />
      </svg>
    ),
  },
  {
    id: "fvg_bear",
    name: "Bearish Fair Value Gap",
    type: "bearish",
    color: "#f87171",
    tag: "IMBALANCE",
    description: "3-candle pattern where a strong bearish candle leaves a gap between candle 1 low and candle 3 high.",
    howToTrade: "Mark the gap between C1 low and C3 high. Enter short when price retraces into the gap. SL above the gap.",
    timeframes: ["5M", "15M", "1H"],
    render: () => (
      <svg viewBox="0 0 200 120" style={{ width: "100%", height: 120 }}>
        <rect width="200" height="120" fill="#080c14" rx="8" />
        {[30,60,90].map(y => <line key={y} x1="10" y1={y} x2="190" y2={y} stroke="#1e293b" strokeWidth="0.5" />)}
        <line x1="45" y1="18" x2="45" y2="52" stroke="#34d399" strokeWidth="1.5" />
        <rect x="38" y="22" width="14" height="22" fill="#34d399" rx="1" />
        <text x="45" y="105" textAnchor="middle" fill="#64748b" fontSize="8">C1</text>
        <line x1="80" y1="20" x2="80" y2="90" stroke="#f87171" strokeWidth="1.5" />
        <rect x="73" y="24" width="14" height="62" fill="#f87171" rx="1" />
        <text x="80" y="105" textAnchor="middle" fill="#f87171" fontSize="8" fontWeight="bold">C2</text>
        <line x1="115" y1="60" x2="115" y2="95" stroke="#f87171" strokeWidth="1.5" />
        <rect x="108" y="64" width="14" height="22" fill="#f87171" rx="1" />
        <text x="115" y="105" textAnchor="middle" fill="#64748b" fontSize="8">C3</text>
        <rect x="62" y="44" width="35" height="18" fill="#f8717120" stroke="#f87171" strokeWidth="1" rx="2" strokeDasharray="3,2" />
        <text x="79" y="56" textAnchor="middle" fill="#f87171" fontSize="7" fontWeight="bold">FVG</text>
        <line x1="38" y1="44" x2="108" y2="44" stroke="#fbbf24" strokeWidth="0.8" strokeDasharray="3,2" />
        <text x="145" y="47" fill="#fbbf24" fontSize="7">C1 Low</text>
        <line x1="108" y1="62" x2="38" y2="62" stroke="#60a5fa" strokeWidth="0.8" strokeDasharray="3,2" />
        <text x="145" y="65" fill="#60a5fa" fontSize="7">C3 High</text>
        <path d="M 130 90 Q 150 68 150 60" stroke="#fbbf24" strokeWidth="1.5" strokeDasharray="3,2" fill="none" />
        <circle cx="150" cy="59" r="3" fill="#fbbf2440" stroke="#fbbf24" strokeWidth="1.5" />
      </svg>
    ),
  },
  {
    id: "choch",
    name: "Change of Character (CHoCH)",
    type: "bullish",
    color: "#60a5fa",
    tag: "REVERSAL SIGNAL",
    description: "Price breaks the last significant swing high/low, signaling a potential trend reversal.",
    howToTrade: "After a downtrend, wait for price to break above a swing high (CHoCH). This signals bullish reversal — look for entry on retest.",
    timeframes: ["5M", "15M", "1H"],
    render: () => (
      <svg viewBox="0 0 200 120" style={{ width: "100%", height: 120 }}>
        <rect width="200" height="120" fill="#080c14" rx="8" />
        {[30,60,90].map(y => <line key={y} x1="10" y1={y} x2="190" y2={y} stroke="#1e293b" strokeWidth="0.5" />)}
        {/* Downtrend */}
        <polyline points="15,20 35,35 55,30 75,50 95,45 115,65" stroke="#f87171" strokeWidth="1.5" fill="none" />
        {[15,35,55,75,95,115].map((x,i) => {
          const ys = [20,35,30,50,45,65];
          return <circle key={i} cx={x} cy={ys[i]} r="3" fill="#f87171" />;
        })}
        {/* Swing high marked */}
        <line x1="55" y1="10" x2="55" y2="30" stroke="#fbbf24" strokeWidth="1" strokeDasharray="3,2" />
        <text x="35" y="9" fill="#fbbf24" fontSize="7">Swing High</text>
        {/* CHoCH break */}
        <polyline points="115,65 130,48 145,30 160,22" stroke="#34d399" strokeWidth="2" fill="none" />
        <line x1="10" y1="30" x2="190" y2="30" stroke="#60a5fa" strokeWidth="1" strokeDasharray="4,3" />
        <text x="100" y="27" fill="#60a5fa" fontSize="8" fontWeight="bold">CHoCH</text>
        {/* Arrow */}
        <polygon points="155,18 160,22 150,22" fill="#34d399" />
        <text x="162" y="24" fill="#34d399" fontSize="7">Break!</text>
      </svg>
    ),
  },
  {
    id: "bos",
    name: "Break of Structure (BOS)",
    type: "bullish",
    color: "#a78bfa",
    tag: "CONTINUATION",
    description: "Price breaks the previous swing high (in uptrend) confirming trend continuation.",
    howToTrade: "After a BOS, look for a pullback to OB or FVG in the direction of the trend. Enter on confirmation.",
    timeframes: ["15M", "1H", "4H"],
    render: () => (
      <svg viewBox="0 0 200 120" style={{ width: "100%", height: 120 }}>
        <rect width="200" height="120" fill="#080c14" rx="8" />
        {[30,60,90].map(y => <line key={y} x1="10" y1={y} x2="190" y2={y} stroke="#1e293b" strokeWidth="0.5" />)}
        <polyline points="15,90 35,65 55,75 75,45 95,55 115,30 135,40 155,15" stroke="#34d399" strokeWidth="1.8" fill="none" />
        {/* HH/HL labels */}
        {[[35,65,"HL"],[55,75,"HL"],[75,45,"HH"],[95,55,"HL"],[115,30,"HH"]].map(([x,y,l],i) => (
          <g key={i}>
            <circle cx={x} cy={y} r="3" fill={l==="HH"?"#a78bfa":"#34d399"} />
            <text x={x} y={y-6} textAnchor="middle" fill={l==="HH"?"#a78bfa":"#34d399"} fontSize="7">{l}</text>
          </g>
        ))}
        {/* BOS line */}
        <line x1="75" y1="45" x2="190" y2="45" stroke="#a78bfa" strokeWidth="1" strokeDasharray="4,3" />
        <text x="130" y="42" fill="#a78bfa" fontSize="8" fontWeight="bold">BOS</text>
        <polygon points="150,11 155,15 145,15" fill="#34d399" />
      </svg>
    ),
  },
  {
    id: "liquidity_sweep",
    name: "Liquidity Sweep",
    type: "bearish",
    color: "#ff6b35",
    tag: "TRAP",
    description: "Price spikes above swing highs or below swing lows to grab stop losses, then reverses sharply.",
    howToTrade: "After a liquidity sweep (wick beyond equal highs/lows), wait for a strong reversal candle + CHoCH. Enter in the reversal direction.",
    timeframes: ["5M", "15M", "1H"],
    render: () => (
      <svg viewBox="0 0 200 120" style={{ width: "100%", height: 120 }}>
        <rect width="200" height="120" fill="#080c14" rx="8" />
        {[30,60,90].map(y => <line key={y} x1="10" y1={y} x2="190" y2={y} stroke="#1e293b" strokeWidth="0.5" />)}
        {/* Equal highs */}
        <line x1="20" y1="40" x2="140" y2="40" stroke="#fbbf24" strokeWidth="1" strokeDasharray="4,2" />
        <text x="5" y="38" fill="#fbbf24" fontSize="7">EQH</text>
        {/* Candles approaching */}
        {[[20,50,75,14],[40,45,72,16],[60,42,70,15],[80,40,68,14]].map(([x,top,bot,body],i) => (
          <g key={i}>
            <line x1={x+6} y1={top} x2={x+6} y2={bot} stroke="#34d399" strokeWidth="1.5" />
            <rect x={x} y={top+2} width="12" height={body} fill="#34d399" rx="1" />
          </g>
        ))}
        {/* Sweep candle */}
        <line x1="106" y1="20" x2="106" y2="72" stroke="#ff6b35" strokeWidth="2" />
        <rect x="100" y="42" width="12" height="22" fill="#f87171" rx="1" />
        <text x="106" y="15" textAnchor="middle" fill="#ff6b35" fontSize="7" fontWeight="bold">SWEEP!</text>
        {/* Reversal */}
        {[[118,45,72,18],[136,52,78,18],[154,62,84,16]].map(([x,top,bot,body],i) => (
          <g key={i}>
            <line x1={x+6} y1={top} x2={x+6} y2={bot} stroke="#f87171" strokeWidth="1.5" />
            <rect x={x} y={top+4} width="12" height={body} fill="#f87171" rx="1" />
          </g>
        ))}
        <text x="155" y="90" fill="#34d399" fontSize="7">Reversal ↓</text>
      </svg>
    ),
  },
  {
    id: "amd_pattern",
    name: "Power of 3 (AMD)",
    type: "neutral",
    color: "#fbbf24",
    tag: "SESSION MODEL",
    description: "Daily price cycle: Accumulate in Asian, Manipulate at session open, Distribute in trend direction.",
    howToTrade: "Mark Asian range. Wait for London/NY to sweep one side (manipulation). Enter in the opposite direction for the distribution move.",
    timeframes: ["15M", "1H"],
    render: () => (
      <svg viewBox="0 0 200 120" style={{ width: "100%", height: 120 }}>
        <rect width="200" height="120" fill="#080c14" rx="8" />
        {/* Sections */}
        <rect x="8" y="10" width="55" height="100" fill="#60a5fa08" rx="4" />
        <rect x="68" y="10" width="45" height="100" fill="#f8717108" rx="4" />
        <rect x="118" y="10" width="75" height="100" fill="#34d39908" rx="4" />
        <text x="35" y="22" textAnchor="middle" fill="#60a5fa" fontSize="7" fontWeight="bold">ACCUMULATE</text>
        <text x="90" y="22" textAnchor="middle" fill="#f87171" fontSize="7" fontWeight="bold">MANIPULATE</text>
        <text x="155" y="22" textAnchor="middle" fill="#34d399" fontSize="7" fontWeight="bold">DISTRIBUTE</text>
        <text x="35" y="110" textAnchor="middle" fill="#60a5fa" fontSize="6">ASIAN</text>
        <text x="90" y="110" textAnchor="middle" fill="#f87171" fontSize="6">LONDON OPEN</text>
        <text x="155" y="110" textAnchor="middle" fill="#34d399" fontSize="6">NEW YORK</text>
        {/* Price action */}
        <polyline points="15,60 25,58 35,62 45,57 55,61" stroke="#60a5fa" strokeWidth="1.5" fill="none" />
        {/* Fake move down */}
        <polyline points="63,61 72,70 80,78 88,85 96,78" stroke="#f87171" strokeWidth="1.5" fill="none" />
        {/* True move up */}
        <polyline points="118,75 128,62 138,50 148,38 158,28 168,22 178,18" stroke="#34d399" strokeWidth="2" fill="none" />
        {/* Asian range lines */}
        <line x1="8" y1="55" x2="63" y2="55" stroke="#60a5fa" strokeWidth="0.8" strokeDasharray="3,2" />
        <line x1="8" y1="63" x2="63" y2="63" stroke="#60a5fa" strokeWidth="0.8" strokeDasharray="3,2" />
        {/* Manipulation zone mark */}
        <text x="85" y="90" textAnchor="middle" fill="#fbbf24" fontSize="7">Stop Hunt</text>
        <circle cx="88" cy="85" r="4" fill="none" stroke="#fbbf24" strokeWidth="1.5" />
      </svg>
    ),
  },
];

export default function ICTApp() {
  const [tab, setTab] = useState("concepts");
  const [selected, setSelected] = useState(null);
  const [checks, setChecks] = useState(Array(checklist.length).fill(false));
  const [bias, setBias] = useState(Array(biasQuestions.length).fill(null));
  const [journalEntries, setJournalEntries] = useState([]);
  const [journalForm, setJournalForm] = useState({ pair: "", bias: "Bullish", rr: "", result: "Win", notes: "" });
  const [patternSelected, setPatternSelected] = useState(null);
  const [patternFilter, setPatternFilter] = useState("all");

  const toggleCheck = (i) => { const c = [...checks]; c[i] = !c[i]; setChecks(c); };
  const checkedCount = checks.filter(Boolean).length;
  const readyToTrade = checkedCount === checklist.length;
  const bullScore = bias.filter((v, i) => v === true && biasQuestions[i].bull).length;
  const bearScore = bias.filter((v, i) => v === false && biasQuestions[i].bull).length;
  const biasResult = bullScore > bearScore ? "BULLISH 🟢" : bearScore > bullScore ? "BEARISH 🔴" : "NEUTRAL ⚪";

  const addJournal = () => {
    if (!journalForm.pair) return;
    setJournalEntries([{ ...journalForm, date: new Date().toLocaleDateString(), id: Date.now() }, ...journalEntries]);
    setJournalForm({ pair: "", bias: "Bullish", rr: "", result: "Win", notes: "" });
  };

  const filteredPatterns = patterns.filter(p => patternFilter === "all" || p.type === patternFilter);

  const tabs = [
    { id: "concepts", label: "Concepts", icon: "📚" },
    { id: "patterns", label: "Patterns", icon: "📈" },
    { id: "checklist", label: "Checklist", icon: "✅" },
    { id: "bias", label: "Bias", icon: "🧭" },
    { id: "journal", label: "Journal", icon: "📓" },
  ];

  return (
    <div style={{ minHeight: "100vh", background: "#080c14", color: "#e2e8f0", fontFamily: "'Courier New', monospace" }}>
      {/* Header */}
      <div style={{ background: "linear-gradient(135deg, #0d1424 0%, #111827 100%)", borderBottom: "1px solid #1e293b", padding: "16px 20px 0", position: "sticky", top: 0, zIndex: 100 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
          <div style={{ width: 32, height: 32, borderRadius: 8, background: "linear-gradient(135deg, #00e5ff, #a78bfa)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, fontWeight: "bold", color: "#000" }}>◈</div>
          <div>
            <div style={{ fontSize: 16, fontWeight: "bold", letterSpacing: 2, color: "#00e5ff" }}>ICT STRATEGY</div>
            <div style={{ fontSize: 9, color: "#64748b", letterSpacing: 3 }}>INNER CIRCLE TRADER</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 2, overflowX: "auto" }}>
          {tabs.map(t => (
            <button key={t.id} onClick={() => setTab(t.id)} style={{
              padding: "7px 12px", border: "none", cursor: "pointer", background: "transparent",
              fontSize: 10, letterSpacing: 1, fontFamily: "inherit", fontWeight: "bold", whiteSpace: "nowrap",
              color: tab === t.id ? "#00e5ff" : "#475569",
              borderBottom: tab === t.id ? "2px solid #00e5ff" : "2px solid transparent", transition: "all 0.2s",
            }}>{t.icon} {t.label.toUpperCase()}</button>
          ))}
        </div>
      </div>

      <div style={{ padding: "20px", maxWidth: 800, margin: "0 auto" }}>

        {/* CONCEPTS */}
        {tab === "concepts" && (
          <div>
            <div style={{ fontSize: 10, color: "#475569", letterSpacing: 3, marginBottom: 16 }}>SELECT A CONCEPT</div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))", gap: 10 }}>
              {concepts.map(c => (
                <button key={c.id} onClick={() => setSelected(selected?.id === c.id ? null : c)} style={{
                  background: selected?.id === c.id ? `${c.color}15` : "#0d1424",
                  border: `1px solid ${selected?.id === c.id ? c.color : "#1e293b"}`,
                  borderRadius: 10, padding: "14px", cursor: "pointer", textAlign: "left",
                  transition: "all 0.2s", color: "#e2e8f0", fontFamily: "inherit",
                }}>
                  <div style={{ fontSize: 22, marginBottom: 6 }}>{c.icon}</div>
                  <div style={{ fontSize: 11, fontWeight: "bold", color: c.color, letterSpacing: 1 }}>{c.label}</div>
                  <div style={{ fontSize: 9, color: "#64748b", marginTop: 3 }}>{c.description.slice(0, 45)}...</div>
                </button>
              ))}
            </div>
            {selected && (
              <div style={{ marginTop: 16, background: "#0d1424", border: `1px solid ${selected.color}40`, borderRadius: 12, padding: 20 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 14 }}>
                  <span style={{ fontSize: 24 }}>{selected.icon}</span>
                  <div>
                    <div style={{ fontSize: 14, fontWeight: "bold", color: selected.color }}>{selected.label}</div>
                    <div style={{ fontSize: 11, color: "#94a3b8" }}>{selected.description}</div>
                  </div>
                </div>
                <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                  {selected.rules.map((r, i) => (
                    <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: 8, padding: "8px 12px", background: "#080c14", borderRadius: 8, fontSize: 12 }}>
                      <span style={{ color: selected.color }}>▸</span>
                      <span style={{ color: "#cbd5e1" }}>{r}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* PATTERNS */}
        {tab === "patterns" && (
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
              <div style={{ fontSize: 10, color: "#475569", letterSpacing: 3 }}>CHART PATTERN VISUAL GUIDE</div>
            </div>
            {/* Filter */}
            <div style={{ display: "flex", gap: 6, marginBottom: 16 }}>
              {["all", "bullish", "bearish", "neutral"].map(f => (
                <button key={f} onClick={() => setPatternFilter(f)} style={{
                  padding: "5px 14px", border: `1px solid ${patternFilter === f ? "#00e5ff" : "#1e293b"}`,
                  background: patternFilter === f ? "#00e5ff15" : "transparent",
                  color: patternFilter === f ? "#00e5ff" : "#475569",
                  borderRadius: 20, cursor: "pointer", fontSize: 9,
                  fontFamily: "inherit", fontWeight: "bold", letterSpacing: 1,
                }}>{f.toUpperCase()}</button>
              ))}
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: 12 }}>
              {filteredPatterns.map(p => (
                <div key={p.id} onClick={() => setPatternSelected(patternSelected?.id === p.id ? null : p)}
                  style={{
                    background: "#0d1424", border: `1px solid ${patternSelected?.id === p.id ? p.color : "#1e293b"}`,
                    borderRadius: 12, overflow: "hidden", cursor: "pointer", transition: "all 0.2s",
                  }}>
                  {/* Chart */}
                  <div style={{ padding: "12px 12px 4px", background: "#080c14" }}>
                    {p.render()}
                  </div>
                  <div style={{ padding: "10px 14px 12px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 4 }}>
                      <div style={{ fontSize: 11, fontWeight: "bold", color: p.color }}>{p.name}</div>
                      <div style={{ fontSize: 8, padding: "2px 7px", borderRadius: 10, background: `${p.color}20`, color: p.color, letterSpacing: 1 }}>{p.tag}</div>
                    </div>
                    <div style={{ fontSize: 10, color: "#64748b", lineHeight: 1.5 }}>{p.description.slice(0, 70)}...</div>
                    <div style={{ display: "flex", gap: 4, marginTop: 8 }}>
                      {p.timeframes.map(tf => (
                        <span key={tf} style={{ fontSize: 8, padding: "2px 6px", background: "#1e293b", color: "#64748b", borderRadius: 4 }}>{tf}</span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {patternSelected && (
              <div style={{ marginTop: 16, background: "#0d1424", border: `1px solid ${patternSelected.color}50`, borderRadius: 12, padding: 20 }}>
                <div style={{ fontSize: 14, fontWeight: "bold", color: patternSelected.color, marginBottom: 6 }}>{patternSelected.name}</div>
                <div style={{ fontSize: 12, color: "#94a3b8", marginBottom: 14, lineHeight: 1.6 }}>{patternSelected.description}</div>
                <div style={{ background: "#080c14", borderRadius: 10, padding: 14, borderLeft: `3px solid ${patternSelected.color}` }}>
                  <div style={{ fontSize: 9, color: "#475569", letterSpacing: 2, marginBottom: 6 }}>HOW TO TRADE</div>
                  <div style={{ fontSize: 12, color: "#cbd5e1", lineHeight: 1.7 }}>{patternSelected.howToTrade}</div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* CHECKLIST */}
        {tab === "checklist" && (
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
              <div style={{ fontSize: 10, color: "#475569", letterSpacing: 3 }}>PRE-TRADE CHECKLIST</div>
              <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <div style={{ fontSize: 12, fontWeight: "bold", color: readyToTrade ? "#4ade80" : "#fbbf24" }}>{checkedCount}/{checklist.length}</div>
                <button onClick={() => setChecks(Array(checklist.length).fill(false))} style={{ background: "#1e293b", border: "none", color: "#64748b", fontSize: 9, padding: "4px 10px", borderRadius: 6, cursor: "pointer", fontFamily: "inherit", letterSpacing: 1 }}>RESET</button>
              </div>
            </div>
            <div style={{ background: "#1e293b", borderRadius: 999, height: 4, marginBottom: 16 }}>
              <div style={{ height: "100%", borderRadius: 999, width: `${(checkedCount / checklist.length) * 100}%`, background: readyToTrade ? "#4ade80" : "linear-gradient(90deg, #00e5ff, #a78bfa)", transition: "width 0.3s ease" }} />
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
              {checklist.map((item, i) => (
                <div key={i} onClick={() => toggleCheck(i)} style={{ display: "flex", alignItems: "center", gap: 12, padding: "12px 14px", background: checks[i] ? "#0d2b1a" : "#0d1424", border: `1px solid ${checks[i] ? "#22c55e40" : "#1e293b"}`, borderRadius: 10, cursor: "pointer", transition: "all 0.2s" }}>
                  <div style={{ width: 18, height: 18, borderRadius: 4, flexShrink: 0, border: `2px solid ${checks[i] ? "#4ade80" : "#334155"}`, background: checks[i] ? "#4ade80" : "transparent", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, color: "#000", transition: "all 0.2s" }}>{checks[i] ? "✓" : ""}</div>
                  <span style={{ fontSize: 12, color: checks[i] ? "#86efac" : "#94a3b8", textDecoration: checks[i] ? "line-through" : "none" }}>{item}</span>
                </div>
              ))}
            </div>
            {readyToTrade && (
              <div style={{ marginTop: 16, padding: 18, background: "#0d2b1a", border: "1px solid #22c55e", borderRadius: 12, textAlign: "center" }}>
                <div style={{ fontSize: 18, marginBottom: 6 }}>✅</div>
                <div style={{ color: "#4ade80", fontWeight: "bold", letterSpacing: 2, fontSize: 12 }}>SETUP CONFIRMED — EXECUTE WITH DISCIPLINE</div>
              </div>
            )}
          </div>
        )}

        {/* BIAS */}
        {tab === "bias" && (
          <div>
            <div style={{ fontSize: 10, color: "#475569", letterSpacing: 3, marginBottom: 16 }}>DAILY BIAS CHECKER</div>
            <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 20 }}>
              {biasQuestions.map((item, i) => (
                <div key={i} style={{ padding: "14px", background: "#0d1424", border: `1px solid ${bias[i] === true ? "#4ade8040" : bias[i] === false ? "#f8717140" : "#1e293b"}`, borderRadius: 10 }}>
                  <div style={{ fontSize: 12, color: "#cbd5e1", marginBottom: 10 }}>{item.q}</div>
                  <div style={{ display: "flex", gap: 6 }}>
                    {["YES", "NO"].map((label, j) => {
                      const val = j === 0; const active = bias[i] === val;
                      return (
                        <button key={label} onClick={() => { const b = [...bias]; b[i] = val; setBias(b); }} style={{ padding: "5px 18px", border: `1px solid ${active ? (val ? "#4ade80" : "#f87171") : "#334155"}`, background: active ? (val ? "#14532d" : "#450a0a") : "transparent", color: active ? (val ? "#4ade80" : "#f87171") : "#64748b", borderRadius: 6, cursor: "pointer", fontSize: 10, fontFamily: "inherit", fontWeight: "bold", letterSpacing: 2, transition: "all 0.15s" }}>{label}</button>
                      );
                    })}
                    <button onClick={() => { const b = [...bias]; b[i] = null; setBias(b); }} style={{ padding: "5px 10px", border: "1px solid #1e293b", background: "transparent", color: "#334155", borderRadius: 6, cursor: "pointer", fontSize: 9, fontFamily: "inherit", letterSpacing: 1 }}>CLR</button>
                  </div>
                </div>
              ))}
            </div>
            <div style={{ padding: 20, background: "#0d1424", border: `1px solid ${biasResult.includes("BULL") ? "#4ade8040" : biasResult.includes("BEAR") ? "#f8717140" : "#334155"}`, borderRadius: 12, textAlign: "center" }}>
              <div style={{ fontSize: 10, color: "#475569", letterSpacing: 3, marginBottom: 6 }}>TODAY'S BIAS</div>
              <div style={{ fontSize: 22, fontWeight: "bold", color: biasResult.includes("BULL") ? "#4ade80" : biasResult.includes("BEAR") ? "#f87171" : "#94a3b8" }}>{biasResult}</div>
              <div style={{ fontSize: 10, color: "#475569", marginTop: 6 }}>Bull: {bullScore} / Bear: {bearScore}</div>
            </div>
          </div>
        )}

        {/* JOURNAL */}
        {tab === "journal" && (
          <div>
            <div style={{ fontSize: 10, color: "#475569", letterSpacing: 3, marginBottom: 16 }}>TRADE JOURNAL</div>
            <div style={{ background: "#0d1424", border: "1px solid #1e293b", borderRadius: 12, padding: 18, marginBottom: 16 }}>
              <div style={{ fontSize: 10, color: "#475569", letterSpacing: 2, marginBottom: 12 }}>LOG NEW TRADE</div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: 8 }}>
                {[{ label: "PAIR", key: "pair", placeholder: "EURUSD" }, { label: "R:R", key: "rr", placeholder: "1:3" }].map(f => (
                  <div key={f.key}>
                    <div style={{ fontSize: 9, color: "#475569", letterSpacing: 2, marginBottom: 3 }}>{f.label}</div>
                    <input value={journalForm[f.key]} onChange={e => setJournalForm({ ...journalForm, [f.key]: e.target.value })} placeholder={f.placeholder} style={{ width: "100%", background: "#080c14", border: "1px solid #1e293b", color: "#e2e8f0", padding: "7px 10px", borderRadius: 8, fontSize: 12, fontFamily: "inherit", boxSizing: "border-box" }} />
                  </div>
                ))}
                {[{ label: "BIAS", key: "bias", opts: ["Bullish", "Bearish"] }, { label: "RESULT", key: "result", opts: ["Win", "Loss", "Breakeven"] }].map(f => (
                  <div key={f.key}>
                    <div style={{ fontSize: 9, color: "#475569", letterSpacing: 2, marginBottom: 3 }}>{f.label}</div>
                    <select value={journalForm[f.key]} onChange={e => setJournalForm({ ...journalForm, [f.key]: e.target.value })} style={{ width: "100%", background: "#080c14", border: "1px solid #1e293b", color: "#e2e8f0", padding: "7px 10px", borderRadius: 8, fontSize: 12, fontFamily: "inherit", boxSizing: "border-box" }}>
                      {f.opts.map(o => <option key={o}>{o}</option>)}
                    </select>
                  </div>
                ))}
              </div>
              <div style={{ marginBottom: 10 }}>
                <div style={{ fontSize: 9, color: "#475569", letterSpacing: 2, marginBottom: 3 }}>NOTES</div>
                <textarea value={journalForm.notes} onChange={e => setJournalForm({ ...journalForm, notes: e.target.value })} placeholder="Setup description..." rows={2} style={{ width: "100%", background: "#080c14", border: "1px solid #1e293b", color: "#e2e8f0", padding: "7px 10px", borderRadius: 8, fontSize: 11, fontFamily: "inherit", resize: "vertical", boxSizing: "border-box" }} />
              </div>
              <button onClick={addJournal} style={{ background: "linear-gradient(135deg, #00e5ff20, #a78bfa20)", border: "1px solid #00e5ff40", color: "#00e5ff", padding: "9px 20px", borderRadius: 8, cursor: "pointer", fontSize: 10, fontFamily: "inherit", fontWeight: "bold", letterSpacing: 2 }}>+ LOG TRADE</button>
            </div>
            {journalEntries.length === 0 ? (
              <div style={{ textAlign: "center", padding: 40, color: "#334155", fontSize: 11, letterSpacing: 2 }}>NO TRADES LOGGED YET</div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
                {journalEntries.map(e => (
                  <div key={e.id} style={{ padding: "12px 14px", background: "#0d1424", border: `1px solid ${e.result === "Win" ? "#22c55e30" : e.result === "Loss" ? "#ef444430" : "#33415530"}`, borderRadius: 10, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <div style={{ display: "flex", gap: 14, alignItems: "center" }}>
                      <div style={{ fontWeight: "bold", color: "#00e5ff", fontSize: 13 }}>{e.pair}</div>
                      <div style={{ fontSize: 10, color: e.bias === "Bullish" ? "#4ade80" : "#f87171" }}>{e.bias}</div>
                      <div style={{ fontSize: 10, color: "#94a3b8" }}>R:R {e.rr}</div>
                    </div>
                    <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
                      <div style={{ fontSize: 9, color: "#475569" }}>{e.date}</div>
                      <div style={{ fontSize: 10, fontWeight: "bold", padding: "2px 9px", borderRadius: 20, background: e.result === "Win" ? "#14532d" : e.result === "Loss" ? "#450a0a" : "#1e293b", color: e.result === "Win" ? "#4ade80" : e.result === "Loss" ? "#f87171" : "#94a3b8" }}>{e.result.toUpperCase()}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
      <style>{`* { box-sizing: border-box; } input::placeholder, textarea::placeholder { color: #334155; } button:hover { opacity: 0.85; } select option { background: #0d1424; }`}</style>
    </div>
  );
}
