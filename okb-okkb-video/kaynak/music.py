import re, numpy as np, wave
from numpy.fft import rfft, irfft
SR = 44100
html = open('index.html', encoding='utf-8').read()
scenes = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\{id:'([\w-]+)',\s*d:(\d+(?:\.\d+)?)", html)]
starts = {}; t = 0.0
for sid, d in scenes: starts[sid] = t; t += d
TOTAL = t
N = int(TOTAL * SR)
rng = np.random.default_rng(7)
def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
tt = np.arange(N) / SR

# ---------- harmony ----------
# Fmaj9, Am7, Cmaj7, G6  (bass, pad notes, arp notes)
CH = [
  (41, [57, 60, 64, 67], [69, 72, 76, 79]),
  (45, [57, 60, 64, 67], [69, 72, 76, 79]),
  (48, [55, 59, 64, 60], [67, 71, 76, 72]),
  (43, [55, 59, 62, 64], [67, 71, 74, 76]),
]
CH[1] = (45, [57, 60, 64, 67], [69, 72, 76, 79])           # Am7: A C E G
CH[0] = (41, [57, 60, 64, 65], [65, 69, 72, 76])           # Fmaj7: F A C E
CHORD_LEN = 8.0
pad = np.zeros((N, 2)); bass = np.zeros(N); arp = np.zeros((N, 2))

def seg_env(n, fade):
    e = np.ones(n); f = int(fade * SR)
    r = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, f))
    e[:f] = r; e[-f:] = r[::-1]; return e

nch = int(np.ceil(TOTAL / CHORD_LEN)) + 1
for k in range(nch):
    b, padn, arpn = CH[k % 4]
    s0 = k * CHORD_LEN - 1.5; s1 = (k + 1) * CHORD_LEN + 1.5
    i0 = max(0, int(s0 * SR)); i1 = min(N, int(s1 * SR))
    if i1 <= i0: continue
    n = i1 - i0; tl = np.arange(n) / SR
    env = seg_env(n, 2.5)
    for j, m in enumerate(padn):
        f = midi(m)
        for det, pan in [(-0.004, -0.6), (0.0, 0.0), (0.004, 0.6)]:
            ph = rng.uniform(0, 2 * np.pi)
            w = np.sin(2*np.pi*f*(1+det)*tl + ph) + 0.22*np.sin(4*np.pi*f*(1+det)*tl + ph) + 0.06*np.sin(6*np.pi*f*(1+det)*tl)
            g = env * 0.028
            pad[i0:i1, 0] += w * g * (1 - pan) / 2 * 2
            pad[i0:i1, 1] += w * g * (1 + pan) / 2 * 2
    fb = midi(b)
    bass[i0:i1] += env * 0.20 * (np.sin(2*np.pi*fb*tl) + 0.15*np.sin(4*np.pi*fb*tl))
lfo = 0.85 + 0.15 * np.sin(2*np.pi*0.06*tt)
pad *= lfo[:, None]

# arpeggio: gentle 8th-ish pattern, 0.75 s per note
pattern = [0, 1, 2, 3, 2, 1]
STEP = 0.75
k = 0; tnote = 4.0
while tnote < TOTAL - 4:
    chord = CH[int(tnote // CHORD_LEN) % 4]
    m = chord[2][pattern[k % len(pattern)]]
    f = midi(m); i0 = int(tnote * SR); L = int(2.4 * SR); i1 = min(N, i0 + L)
    tl = np.arange(i1 - i0) / SR
    e = np.exp(-tl / 0.85) * (1 - np.exp(-tl / 0.004))
    w = (np.sin(2*np.pi*f*tl) + 0.25*np.sin(4*np.pi*f*tl) + 0.07*np.sin(6*np.pi*f*tl)) * e
    vel = 0.050 * (1.0 if k % 6 == 0 else 0.75) * rng.uniform(0.85, 1.0)
    pan = 0.3 if k % 2 else -0.3
    arp[i0:i1, 0] += w * vel * (1 - pan); arp[i0:i1, 1] += w * vel * (1 + pan)
    k += 1; tnote += STEP
# arp swells in after the title, rests slightly on dense reading scenes
arp_gain = np.clip((tt - 4) / 6, 0, 1)
arp *= arp_gain[:, None]

# ---------- sfx ----------
sfx = np.zeros((N, 2))
def add(sig, at, gain=1.0, pan=0.0):
    i0 = int(at * SR); i1 = min(N, i0 + len(sig))
    if i0 >= N: return
    s = sig[:i1 - i0] * gain
    sfx[i0:i1, 0] += s * (1 - pan); sfx[i0:i1, 1] += s * (1 + pan)

def whoosh(dur=0.9):
    n = int(dur * SR); x = rng.standard_normal(n)
    # time-varying one-pole lowpass sweep (dark -> bright -> dark)
    pos = np.linspace(0, 1, n); fc = 300 + 2600 * np.sin(np.pi * pos) ** 2
    a = np.exp(-2*np.pi*fc/SR); y = np.zeros(n); acc = 0.0
    for i in range(n):
        acc = (1 - a[i]) * x[i] + a[i] * acc; y[i] = acc
    env = np.sin(np.pi * pos) ** 2
    return y * env / (np.abs(y).max() + 1e-9)

def bell(f0=1046.5, dur=2.6):
    n = int(dur * SR); tl = np.arange(n) / SR
    parts = [(1.0, 1.0, 1.6), (2.0, 0.45, 0.9), (2.76, 0.32, 0.7), (5.40, 0.16, 0.35), (8.93, 0.08, 0.2)]
    y = sum(a * np.sin(2*np.pi*f0*r*tl) * np.exp(-tl/d) for r, a, d in parts)
    y *= (1 - np.exp(-tl / 0.002))
    return y / np.abs(y).max()

def thump(dur=0.5):
    n = int(dur * SR); tl = np.arange(n) / SR
    f = 95 * np.exp(-tl / 0.12) + 45
    ph = 2*np.pi*np.cumsum(f)/SR
    y = np.sin(ph) * np.exp(-tl / 0.13)
    click = rng.standard_normal(n) * np.exp(-tl / 0.008) * 0.35
    return (y + click) / 1.2

W = whoosh()
for sid, _ in scenes[1:]:
    add(W, starts[sid] - 0.45, gain=0.045, pan=0.0)

B = bell()
a0 = starts['s-alarm'] + 0.9
for i, dt in enumerate([0.0, 0.32, 0.64, 0.96]):
    add(B, a0 + dt, gain=0.085 * (1 - 0.15 * i), pan=(-0.25 if i % 2 else 0.25))
add(B, starts['s-close'] + 1.0, gain=0.07, pan=-0.2)
add(B, starts['s-close'] + 1.32, gain=0.055, pan=0.2)
T = thump()
add(T, starts['s-ece'] + 14.45, gain=0.30)
add(T, starts['s-kerem'] + 14.45, gain=0.30)
# soft "page" tick for each rule line appearing
tick = whoosh(0.12)
for i in range(8):
    add(tick, starts['s-rules'] + 2.8 + 0.75 * i, gain=0.018, pan=0.3)

# ---------- reverb (convolution with synthetic IR) ----------
def ir(seconds=2.8, seed=1):
    r = np.random.default_rng(seed); n = int(seconds * SR); tl = np.arange(n) / SR
    x = r.standard_normal(n) * np.exp(-tl / (seconds / 6.9))
    # darken
    y = np.convolve(x, np.ones(6) / 6, mode='same')
    y[:int(0.012*SR)] = 0
    return y / np.sqrt((y**2).sum())
def conv(x, h):
    L = len(x) + len(h) - 1; nfft = 1 << (L - 1).bit_length()
    return irfft(rfft(x, nfft) * rfft(h, nfft), nfft)[:len(x)]
dry = pad + arp
send = pad * 0.6 + arp + sfx * 0.6
wet = np.stack([conv(send[:, 0], ir(seed=1)), conv(send[:, 1], ir(seed=2))], axis=1)
mix = dry + sfx + bass[:, None] + wet * 0.55

# fades
fi = np.clip(tt / 2.0, 0, 1); fo = np.clip((TOTAL - tt) / 3.0, 0, 1)
mix *= (fi * fo)[:, None]
mix = np.tanh(mix * 1.2) / 1.2
mix /= np.abs(mix).max() / 0.89
pcm = (mix * 32767).astype(np.int16)
with wave.open('music_raw.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('TOTAL', TOTAL, 'samples', N)
