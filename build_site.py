import re, base64

raw_path = 'C:/Users/TUF GAMING/code-demo/kuru-ocean-studio/clean_source.html'
with open(raw_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CSS styling (Tanpa section portfolio)
new_css = """
/* --- TESTIMONIALS & DISCORD OWNER STYLES --- */
.testimonials{max-width:1100px;margin:30px auto 40px;padding:60px 30px;position:relative}
.testimonials-head{text-align:center;max-width:640px;margin:0 auto 40px}
.testimonials-head .eyebrow{color:var(--aqua);letter-spacing:.14em;font-size:12px;text-transform:uppercase;margin-bottom:8px}
.testimonials-head h2{font-size:36px;line-height:1.2;margin:0 0 14px;color:#ecfdff;letter-spacing:-.03em}
.testimonials-head p{font-size:16px;line-height:1.6;color:#9ec2c9;margin:0}
.testimonials-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
.testimonial-card{background:#082435;border:1px solid #1e4a5f;border-radius:24px;padding:30px 26px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 10px 32px rgba(0,0,0,.25);transition:transform .3s ease,box-shadow .3s ease,border-color .3s ease;position:relative;overflow:hidden}
.testimonial-card:hover{transform:translateY(-4px);box-shadow:0 18px 45px rgba(0,169,189,.2);border-color:var(--aqua)}
.testimonial-card::before{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,var(--blue),var(--aqua))}
.testimonial-quote{font-size:15px;line-height:1.65;color:#def4f6;margin:0 0 24px;font-style:italic}
.testimonial-quote::before{content:"“";font-size:36px;line-height:0;margin-right:4px;vertical-align:-10px;color:var(--aqua);font-family:Georgia,serif}
.testimonial-quote::after{content:"”";font-size:36px;line-height:0;margin-left:4px;vertical-align:-10px;color:var(--aqua);font-family:Georgia,serif}
.discord-card{display:flex;align-items:center;gap:14px;padding:12px 16px;background:#051a27;border:1px solid #1b455b;border-radius:16px;text-decoration:none;color:inherit;transition:background .2s,border-color .2s}
.discord-card:hover{background:#092a3e;border-color:var(--aqua)}
.discord-avatar{width:46px;height:46px;border-radius:50%;background:#5865F2;display:flex;align-items:center;justify-content:center;color:#fff;flex-shrink:0;box-shadow:0 4px 12px rgba(88,101,242,.35);overflow:hidden}
.discord-avatar svg{width:26px;height:26px;fill:currentColor}
.discord-meta{display:flex;flex-direction:column;min-width:0;flex:1}
.discord-tag{font-size:14px;font-weight:700;color:#ecfdff;letter-spacing:-.01em;display:flex;align-items:center;gap:6px}
.discord-badge{font-size:10px;padding:2px 7px;border-radius:999px;background:#5865f225;color:#8ba2ff;font-weight:600;border:1px solid rgba(88,101,242,.3)}
.discord-id{font-family:monospace;font-size:12px;color:#85a9b2;letter-spacing:.02em;margin-top:2px}
.discord-link-icon{color:#85a9b2;font-size:16px;margin-left:auto;transition:transform .2s,color .2s}
.discord-card:hover .discord-link-icon{transform:translateX(3px);color:var(--aqua)}

/* Owner profile card in contact / closing */
.owner-discord-wrap{margin:20px 0 26px;display:flex;justify-content:center}
.owner-card{display:inline-flex;align-items:center;gap:14px;padding:12px 20px;background:rgba(2,15,28,.85);border:1px solid #1e4a5f;border-radius:20px;text-decoration:none;transition:transform .25s,border-color .25s,box-shadow .25s}
.owner-card:hover{transform:translateY(-2px);border-color:var(--aqua);box-shadow:0 8px 24px rgba(66,185,204,.25)}
.owner-avatar{width:48px;height:48px;border-radius:50%;overflow:hidden;border:2px solid var(--aqua);flex-shrink:0;box-shadow:0 0 14px rgba(143,240,230,.3)}
.owner-avatar img{width:100%;height:100%;object-fit:cover;display:block}
.owner-meta{display:flex;flex-direction:column;text-align:left}
.owner-name{font-size:15px;font-weight:700;color:#fff;display:flex;align-items:center;gap:6px}
.owner-sub{font-size:12px;color:#85a9b2;font-family:monospace;margin-top:2px}

@media(max-width:700px){
 .testimonials{padding:40px 16px;margin:10px 0 20px}
 .testimonials-head h2{font-size:28px}
 .testimonials-grid{grid-template-columns:1fr;gap:16px}
 .testimonial-card{padding:24px 20px}
 .owner-discord-wrap{justify-content:flex-start}
}
"""

# 2. Section HTML Testimoni (tanpa grid gambar karya)
testi_html = """
<!-- TESTIMONI KLIEN -->
<section class="testimonials" id="testimonials" aria-labelledby="testi-title">
 <div class="testimonials-head">
  <p class="eyebrow">Testimoni Klien</p>
  <h2 id="testi-title">Apa kata mereka?</h2>
  <p>Pengalaman kolaborasi pengerjaan art commission, custom web, dan Minecraft project bersama Kuru Studio.</p>
 </div>
 <div class="testimonials-grid">
  <article class="testimonial-card">
   <p class="testimonial-quote">Hasil commission rapi banget, detail sesuai brief dari awal, dan komunikasinya enak tanpa ribet. Recomended banget!</p>
   <a class="discord-card" href="https://discord.com/users/921611802855481436" target="_blank" rel="noopener noreferrer" aria-label="Buka profil Discord klien 921611802855481436">
    <div class="discord-avatar"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994.021-.041.001-.09-.041-.106a13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.929 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.893.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg></div>
    <div class="discord-meta">
     <div class="discord-tag"><span>Camwynn</span><span class="discord-badge">Verified</span></div>
     <div class="discord-id">ID: 921611802855481436</div>
    </div>
    <span class="discord-link-icon" aria-hidden="true">↗</span>
   </a>
  </article>
  <article class="testimonial-card">
   <p class="testimonial-quote">Pengerjaan video motion dan asetnya presisi, revisi ditanggapi cepat, dan delivery selalu tepat waktu. Keren pol!</p>
   <a class="discord-card" href="https://discord.com/users/1043076281316683856" target="_blank" rel="noopener noreferrer" aria-label="Buka profil Discord klien 1043076281316683856">
    <div class="discord-avatar"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994.021-.041.001-.09-.041-.106a13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.929 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.893.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg></div>
    <div class="discord-meta">
     <div class="discord-tag"><span>ggsyamandi</span><span class="discord-badge">Verified</span></div>
     <div class="discord-id">ID: 1043076281316683856</div>
    </div>
    <span class="discord-link-icon" aria-hidden="true">↗</span>
   </a>
  </article>
 </div>
</section>
"""

# A. Insert CSS
assert '</style>' in html
html = html.replace('</style>', new_css + '\n</style>', 1)

# B. Insert Testimonials RIGHT AFTER the closing </div> of #services
grid_end = '</div>\n<section class="process" id="process">'
if grid_end not in html:
    grid_end = '</div><section class="process" id="process">'
assert grid_end in html, 'Could not find grid end for #services'
html = html.replace(grid_end, '</div>\n' + testi_html + '\n<section class="process" id="process">', 1)

# C. Update Navigation links to include Testimoni
old_nav = '<a href="#services">Layanan</a><a href="#process">Cara Order</a>'
new_nav = '<a href="#services">Layanan</a><a href="#testimonials">Testimoni</a><a href="#process">Cara Order</a>'
assert old_nav in html
html = html.replace(old_nav, new_nav, 1)

# D. Update Footer links
old_footer = '<a href="#art">Art</a> &nbsp; / &nbsp; <a href="#development">Development</a> &nbsp; / &nbsp; <a href="#process">Cara Order</a>'
new_footer = '<a href="#art">Art</a> &nbsp; / &nbsp; <a href="#services">Layanan</a> &nbsp; / &nbsp; <a href="#testimonials">Testimoni</a> &nbsp; / &nbsp; <a href="#process">Cara Order</a>'
if old_footer in html:
    html = html.replace(old_footer, new_footer, 1)

# E. Add Discord Profile Card to #contact (Closing section)
owner_discord_card = """
<div class="owner-discord-wrap">
 <a class="owner-card" href="https://discord.com/users/1358345285482319892" target="_blank" rel="noopener noreferrer" aria-label="Buka profil Discord himmell_">
  <div class="owner-avatar"><img src="assets/discord-avatar.png" alt="Discord Profile himmell_"></div>
  <div class="owner-meta">
   <span class="owner-name">himmell_ <span class="discord-badge">Admin &amp; Dev</span></span>
   <span class="owner-sub">Discord ID: 1358345285482319892</span>
  </div>
  <span class="discord-link-icon" aria-hidden="true" style="color:var(--aqua)">↗</span>
 </a>
</div>
"""

closing_actions = '<div class="actions"><a class="btn" href="https://www.instagram.com/favv.vrk/" target="_blank" rel="noopener noreferrer">Instagram ↗</a>'
assert closing_actions in html
html = html.replace(closing_actions, owner_discord_card + '\n<div class="actions"><a class="btn" href="https://www.instagram.com/favv.vrk/" target="_blank" rel="noopener noreferrer">Instagram ↗</a>', 1)

# F. Add .testimonial-card to reveal animation in CSS & JS
old_reveal_css = '.panel-copy,.artwork,.browser,.tile>svg,.code-window,.process>div,.steps li,.closing{transition:opacity .8s,translate .8s cubic-bezier(.22,1,.36,1)}'
new_reveal_css = '.panel-copy,.artwork,.browser,.tile>svg,.code-window,.testimonial-card,.process>div,.steps li,.closing{transition:opacity .8s,translate .8s cubic-bezier(.22,1,.36,1)}'
assert old_reveal_css in html
html = html.replace(old_reveal_css, new_reveal_css, 1)

old_reveal_js = ".panel-copy,.artwork,.browser,.tile>svg,.code-window,.process>div,.steps li,.closing"
new_reveal_js = ".panel-copy,.artwork,.browser,.tile>svg,.code-window,.testimonial-card,.process>div,.steps li,.closing"
assert old_reveal_js in html
html = html.replace(old_reveal_js, new_reveal_js, 1)

# Encrypt to index.html
key = 107
encoded_bytes = bytes([b ^ key for b in html.encode('utf-8')])
b64_str = base64.b64encode(encoded_bytes).decode('ascii')

final_encrypted_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kuru Studio — Art &amp; Development</title>
<link rel="icon" href="assets/jellyfish-icon.svg?v=1" type="image/svg+xml">
<style>html,body{{background:#0b0c10;color:#fff;margin:0;padding:0;height:100%}}</style>
<script>
(function(){{
  function _k(e){{
    if((e.ctrlKey||e.metaKey)&&["u","U","s","S","p","P"].indexOf(e.key)!==-1){{
      e.preventDefault();e.stopPropagation();return false;
    }}
    if(e.key==="F12"||((e.ctrlKey||e.metaKey)&&e.shiftKey&&["I","i","J","j","C","c","K","k"].indexOf(e.key)!==-1)){{
      e.preventDefault();e.stopPropagation();return false;
    }}
  }}
  window.addEventListener("keydown",_k,true);
  document.addEventListener("contextmenu",function(e){{e.preventDefault();e.stopPropagation();return false;}},true);
}})();
</script>
</head>
<body>
<noscript><div style="text-align:center;padding:50px;font-family:sans-serif;color:#fff;">Aktifkan JavaScript untuk membuka website ini.</div></noscript>
<script>
/* Source Code Protected & Encrypted */
(function(){{
  var _k = {key};
  var _d = "{b64_str}";
  try {{
    var _r = atob(_d);
    var _u = new Uint8Array(_r.length);
    for (var i = 0; i < _r.length; i++) {{
      _u[i] = _r.charCodeAt(i) ^ _k;
    }}
    var _h = new TextDecoder("utf-8").decode(_u);
    document.open();
    document.write(_h);
    document.close();
  }} catch(e) {{
    document.body.innerHTML = "Access Restricted.";
  }}
}})();
</script>
</body>
</html>"""

with open('C:/Users/TUF GAMING/code-demo/kuru-ocean-studio/index.html', 'w', encoding='utf-8') as f_idx:
    f_idx.write(final_encrypted_html)

print('Updated and protected index.html without portfolio images successfully!')
