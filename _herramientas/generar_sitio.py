#!/usr/bin/env python3
"""Genera el sitio estático de Marcela Córdoba (GitHub Pages).
Uso: python3 build.py <carpeta-del-repo>"""
import sys, os, json, html
from urllib.parse import quote

OUT = sys.argv[1]
SITE = 'https://marcelacordoba.com'

# ---------------------------------------------------------------- helpers
import re, unicodedata
def slug(f):
    b = os.path.splitext(f)[0]
    b = unicodedata.normalize('NFKD', b).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', b).strip('-')

def esc(s): return html.escape(s, quote=True)

ICONS = {
 'fb': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg>',
 'ig': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor" stroke="none"/></svg>',
 'in': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-4 0v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/></svg>',
 'yt': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22.54 6.42a2.78 2.78 0 00-1.95-1.96C18.88 4 12 4 12 4s-6.88 0-8.59.46a2.78 2.78 0 00-1.95 1.96A29 29 0 001 12a29 29 0 00.46 5.58A2.78 2.78 0 003.41 19.6C5.12 20 12 20 12 20s6.88 0 8.59-.46a2.78 2.78 0 001.95-1.95A29 29 0 0023 12a29 29 0 00-.46-5.58zM9.75 15.02V8.98L15.5 12l-5.75 3.02z"/></svg>',
 'wa': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.1c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3zM12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm0 18.2c-1.5 0-3-.4-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1112 20.2z"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="3"/><path d="m22 7-10 6L2 7"/></svg>',
 'pin': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s-7-6.2-7-12a7 7 0 1114 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 'check': '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
}
SOCIAL = [
 ('fb', 'Facebook', 'https://www.facebook.com/profile.php?id=100073081083737'),
 ('ig', 'Instagram', 'https://www.instagram.com/marcelacordobamentora/'),
 ('in', 'LinkedIn', 'https://www.linkedin.com/in/marcelacordobamentora/'),
 ('yt', 'YouTube', 'https://www.youtube.com/@Marcelacordobamentora'),
]

PAGES_NAV = {
 'inicio': '', 'sobre': 'sobre-marcela/', 'idrea': 'modelo-idrea/', 'recursos': 'recursos/', 'contacto': 'contacto/',
 'personal': 'coaching-personal/', 'lideres': 'coaching-lideres/', 'formacion': 'formacion-desarrollo-talento/', 'seleccion': 'seleccion-talento/',
}

def socials_html():
    return ''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{ICONS[k]}</a>' for k, n, u in SOCIAL)

def header(r, active):
    def cur(k): return ' aria-current="page"' if active == k else ''
    serv_active = ' aria-current="page"' if active in ('personal', 'lideres', 'formacion', 'seleccion') else ''
    L = lambda k: r + PAGES_NAV[k]
    return f'''<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="nav" id="nav">
  <div class="wrap nav-inner">
    <a href="{L('inicio') or './'}" class="nav-logo" aria-label="Marcela Córdoba — Inicio"><img src="{r}img/logo.png" alt="Marcela Córdoba" width="566" height="115" /></a>
    <button class="burger" id="burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    <nav aria-label="Principal">
      <ul class="nav-menu" id="menu">
        <li><a class="nav-link" href="{L('inicio') or './'}"{cur('inicio')}>Inicio</a></li>
        <li><a class="nav-link" href="{L('sobre')}"{cur('sobre')}>Sobre Marcela</a></li>
        <li class="has-sub">
          <button class="nav-link" aria-expanded="false" aria-haspopup="true"{serv_active}>Servicios <i class="caret" aria-hidden="true"></i></button>
          <div class="sub">
            <div>
              <p class="sub-label">Personas</p>
              <a href="{L('personal')}">Coaching personal<small>Claridad, patrones y resultados</small></a>
            </div>
            <div>
              <p class="sub-label">Empresas</p>
              <a href="{L('lideres')}">Coaching para líderes<small>Liderazgo consciente</small></a>
              <a href="{L('formacion')}">Formación y desarrollo de talento<small>Talleres y programas</small></a>
              <a href="{L('seleccion')}">Atracción y selección de talento<small>La persona adecuada</small></a>
            </div>
          </div>
        </li>
        <li><a class="nav-link" href="{L('idrea')}"{cur('idrea')}>Modelo IDREA®</a></li>
        <li><a class="nav-link" href="{L('recursos')}"{cur('recursos')}>Recursos</a></li>
        <li><a class="btn btn-primary nav-cta" href="{L('contacto')}">Contacto</a></li>
      </ul>
    </nav>
  </div>
</header>'''

def footer(r):
    L = lambda k: r + PAGES_NAV[k]
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <p>“Los resultados extraordinarios comienzan en las personas que los crean.”</p>
        <div class="socials">{socials_html()}</div>
      </div>
      <div>
        <h4>Personas</h4>
        <ul><li><a href="{L('personal')}">Coaching personal</a></li><li><a href="{L('idrea')}">Modelo IDREA®</a></li><li><a href="{L('recursos')}">Libro y testimonios</a></li></ul>
      </div>
      <div>
        <h4>Empresas</h4>
        <ul><li><a href="{L('lideres')}">Coaching para líderes</a></li><li><a href="{L('formacion')}">Formación y desarrollo</a></li><li><a href="{L('seleccion')}">Selección de talento</a></li></ul>
      </div>
      <div>
        <h4>Contacto</h4>
        <ul>
          <li><a href="{L('contacto')}">Escríbenos</a></li>
          <li data-wa-wrap><a data-wa href="#" target="_blank" rel="noopener">WhatsApp</a></li>
          <li data-email-wrap><a data-email href="#"></a></li>
          <li>Cali, Colombia · Atención en LATAM</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© <span id="year">2026</span> Marcela Córdoba. Todos los derechos reservados.</p>
      <nav aria-label="Legal"><a href="{r}politica-de-datos/">Política de tratamiento de datos</a></nav>
    </div>
  </div>
</footer>'''

def page(path, title, desc, active, body, mobile_cta=None, jsonld=None, noindex=False):
    depth = path.count('/')
    r = '../' * depth
    canon = SITE + '/' + path
    mcta = f'<div class="mobile-cta"><a class="btn btn-primary" href="{mobile_cta[1]}">{esc(mobile_cta[0])}</a></div>' if mobile_cta else ''
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ''
    robots = '<meta name="robots" content="noindex" />' if noindex else ''
    doc = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  {robots}
  <link rel="canonical" href="{canon}" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="es_CO" />
  <meta property="og:site_name" content="Marcela Córdoba" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:image" content="{SITE}/img/og-image.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="theme-color" content="#2B1747" />
  <link rel="icon" href="{r}favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="{r}favicon-32.png" sizes="32x32" type="image/png" />
  <link rel="apple-touch-icon" href="{r}apple-touch-icon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{r}styles.css" />
  {ld}
</head>
<body>
{header(r, active)}
<main id="contenido">
{body.replace('{R}', r)}
</main>
{footer(r)}
{mcta}
<script src="{r}config.js"></script>
<script src="{r}script.js"></script>
</body>
</html>
'''
    import re as _re
    doc = _re.sub(r'(<h[123][^>]*>)(.*?)(</h[123]>)', lambda m: m.group(1) + m.group(2).replace('®', '<sup>®</sup>') + m.group(3), doc, flags=_re.S)
    dest = os.path.join(OUT, path, 'index.html') if path else os.path.join(OUT, 'index.html')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(doc)

def hero(eyebrow, title_html, lead, buttons, img, alt, badge=None, flip=False, page_hero=True, proof=None):
    btns = ''.join(f'<a class="btn {cls}" href="{href}">{esc(t)}</a>' for t, href, cls in buttons)
    b = f'<div class="portal-badge">{badge}</div>' if badge else ''
    pr = ''
    if proof:
        pr = '<div class="hero-proof">' + ''.join(f'<div><strong>{a}</strong><span>{b_}</span></div>' for a, b_ in proof) + '</div>'
    return f'''<section class="hero{' page-hero' if page_hero else ''}">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">{eyebrow}</p>
      <h1 class="h1">{title_html}</h1>
      <p class="lead">{lead}</p>
      <div class="btn-row">{btns}</div>
      {pr}
    </div>
    <div class="portal{' flip' if flip else ''}">
      <img src="{{R}}img/{img}" alt="{esc(alt)}" fetchpriority="high" />
      {b}
    </div>
  </div>
</section>'''

def checks(items, cls=''):
    return f'<ul class="checks {cls}">' + ''.join(f'<li class="reveal">{esc(i)}</li>' for i in items) + '</ul>'

def section_head(eyebrow, title_html, lead=None, center=False):
    l = f'<p class="lead">{lead}</p>' if lead else ''
    return f'<div class="section-head{" center" if center else ""} reveal"><p class="eyebrow">{eyebrow}</p><h2 class="h2">{title_html}</h2>{l}</div>'

def cta_band(title_html, text, btn, href):
    return f'''<section class="section tight bg-paper"><div class="wrap"><div class="cta-band reveal">
  <h2 class="h2">{title_html}</h2><p>{text}</p>
  <div class="btn-row"><a class="btn btn-light" href="{href}">{esc(btn)}</a></div>
</div></div></section>'''

def statement(tag, text_html, bg='bg-plum'):
    return f'<section class="section tight {bg}"><div class="wrap statement reveal"><p class="tag">{tag}</p><blockquote>{text_html}</blockquote></div></section>'

# ---------------------------------------------------------------- formularios
def field(f):
    name, label, kind = f['name'], f['label'], f.get('type', 'text')
    req = f.get('req', False)
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ''
    rq = ' required' if req else ''
    full = ' full' if f.get('full') else ''
    fid = 'f-' + name + '-' + f['_form']
    ph = f' placeholder="{esc(f["ph"])}"' if f.get('ph') else ''
    ac = f' autocomplete="{f["ac"]}"' if f.get('ac') else ''
    hint = f'<span class="hint">{esc(f["hint"])}</span>' if f.get('hint') else ''
    if kind == 'chips':
        opts = ''.join(f'<label><input type="radio" name="{name}" value="{esc(o)}"{rq if i == 0 else ""} /><span>{esc(o)}</span></label>' for i, o in enumerate(f['opts']))
        return f'<fieldset class="field chips{full}"><legend>{esc(label)}{star}</legend>{opts}</fieldset>'
    if kind == 'select':
        opts = '<option value="" disabled selected>Selecciona una opción</option>' + ''.join(f'<option>{esc(o)}</option>' for o in f['opts'])
        return f'<div class="field{full}"><label for="{fid}">{esc(label)}{star}</label><select class="input" id="{fid}" name="{name}"{rq}>{opts}</select>{hint}</div>'
    if kind == 'textarea':
        return f'<div class="field{full}"><label for="{fid}">{esc(label)}{star}</label><textarea class="input" id="{fid}" name="{name}" rows="3" maxlength="1200"{rq}{ph}></textarea>{hint}</div>'
    extra = ''
    if kind == 'number': extra = ' min="1" inputmode="numeric"'
    if kind == 'tel': extra = ' inputmode="tel"'
    return f'<div class="field{full}"><label for="{fid}">{esc(label)}{star}</label><input class="input" type="{kind}" id="{fid}" name="{name}"{ac}{ph}{extra}{rq} />{hint}</div>'

def form_block(key, service, title_html, lead, fields, more, submit, r_hint='{R}', reassure=None):
    for f in fields + more: f['_form'] = key
    main = ''.join(field(f) for f in fields)
    extra = ''
    if more:
        extra = f'<details><summary>Agregar más detalles (opcional)</summary><div class="more">{"".join(field(f) for f in more)}</div></details>'
    rs = reassure or ['Sin crear cuentas ni pagos por adelantado.', 'Te contactamos para entender tu situación y definir el siguiente paso.', 'Tus datos se usan solo para responder tu solicitud.']
    rs_html = '<ul class="reassure">' + ''.join(f'<li>{esc(x)}</li>' for x in rs) + '</ul>'
    return f'''<section class="section form-section" id="formulario">
  <div class="wrap form-layout">
    <div class="form-aside reveal">
      <p class="eyebrow">Da el primer paso</p>
      <h2 class="h2">{title_html}</h2>
      <p class="lead">{lead}</p>
      {rs_html}
    </div>
    <div class="form-card reveal">
      <form class="lead-form" data-service="{esc(service)}" novalidate>
        <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" />
        {main}
        {extra}
        <label class="consent field"><input type="checkbox" name="autorizacion_datos" value="Sí autorizo" required /><span>Autorizo el tratamiento de mis datos personales conforme a la <a href="{r_hint}politica-de-datos/" target="_blank">Política de tratamiento de datos</a>. <span class="req" aria-hidden="true">*</span></span></label>
        <div class="form-error" role="alert"></div>
        <div class="form-foot">
          <button type="submit" class="btn btn-primary btn-block">{esc(submit)}</button>
          <small><span class="req">*</span> Campos obligatorios</small>
        </div>
      </form>
      <div class="form-success" role="status" aria-live="polite">
        <div class="seal">{ICONS['check']}</div>
        <h3>Gracias. Ya diste el primer paso.</h3>
        <p>Recibimos tu información. Revisaremos tu solicitud y nos pondremos en contacto contigo para conocer mejor tu situación y definir el siguiente paso.</p>
      </div>
    </div>
  </div>
</section>'''

ORIGEN = {'name': 'como_nos_conocio', 'label': '¿Cómo te enteraste de Marcela?', 'type': 'select', 'opts': ['Instagram', 'LinkedIn', 'Facebook', 'YouTube', 'Google', 'Recomendación', 'Evento o conferencia', 'Libro', 'Otro']}
ORIGEN_E = dict(ORIGEN, label='¿Cómo conocieron a Marcela?')
MODALIDAD = {'name': 'modalidad', 'label': 'Modalidad preferida', 'type': 'chips', 'opts': ['Virtual', 'Presencial', 'Por definir'], 'full': True}

def company_base():
    return [
        {'name': 'empresa', 'label': 'Nombre de la empresa', 'req': True, 'ac': 'organization'},
        {'name': 'nombre', 'label': 'Nombre de quien solicita', 'req': True, 'ac': 'name'},
        {'name': 'cargo', 'label': 'Cargo', 'req': True, 'ac': 'organization-title'},
        {'name': 'correo', 'label': 'Correo corporativo', 'type': 'email', 'req': True, 'ac': 'email'},
        {'name': 'whatsapp', 'label': 'WhatsApp / teléfono', 'type': 'tel', 'req': True, 'ac': 'tel'},
    ]

AUTH = [
    ('Psicóloga', 'Pontificia Universidad Javeriana'),
    ('Coach certificada', 'internacionalmente'),
    ('Mentora y consultora', 'en transformación personal y organizacional'),
    ('Creadora del Modelo IDREA®', ''),
    ('Autora', 'de RESULTADOS EXTRAORDINARIOS'),
    ('Conferencista', 'internacional'),
]

def authority_block(r='{R}', heading='¿Por qué <em>Marcela</em>?', eyebrow='Autoridad'):
    lis = ''.join(f'<li><strong>{a}</strong> {b}</li>' for a, b in AUTH)
    return f'''<section class="section bg-white">
  <div class="wrap authority">
    <div class="reveal">
      <p class="eyebrow">{eyebrow}</p>
      <h2 class="h2">{heading}</h2>
      <ul class="cred-list">{lis}</ul>
    </div>
    <div class="reveal">
      <div class="stats-band">
        <div><strong>+15</strong><span>años de experiencia</span></div>
        <div><strong>+2.500</strong><span>personas entrenadas</span></div>
        <div><strong>+10</strong><span>países con empresas y equipos acompañados</span></div>
      </div>
    </div>
  </div>
</section>'''

def how_to_hire(kind):
    if kind == 'persona':
        s = [('Cuéntanos tu situación', 'Diligencia el formulario. Toma pocos minutos.'),
             ('Conversación inicial', 'Te contactamos para entender qué quieres transformar.'),
             ('Tu programa', 'Definimos juntos el nivel de acompañamiento adecuado y comienzas.')]
    else:
        s = [('Cuéntenos la necesidad', 'Diligencien el formulario con el contexto y el resultado esperado.'),
             ('Reunión de diagnóstico', 'Agendamos una conversación para entender el reto a fondo.'),
             ('Propuesta a la medida', 'Presentamos la solución, alcance y cronograma para iniciar.')]
    steps = ''.join(f'<div class="step reveal"><h3>{a}</h3><p>{b}</p></div>' for a, b in s)
    return f'''<section class="section bg-cream">
  <div class="wrap">
    {section_head('Cómo contratar', '¿Cómo <em>empezamos</em>?', center=True)}
    <div class="steps" style="--n:3">{steps}</div>
  </div>
</section>'''

LOGOS = ['LOGO AA SAS.jpg', 'LOGO CONTINENTAL DE INGREDIENTES.jpeg', 'LOGO ED 2019.png', 'Lockton Sekuritas.jpeg', 'logoSanJorge.png', 'Logo Eniwork.jpeg', 'Logo Ensalud.jpeg', 'Logo Los Olivos.jpeg', 'Logo Procaps.jpeg', 'Logo Rutina.jpeg', 'Logo Sushi Break 1.jpg', 'Manufacturas Economicas.png', 'QI ENERGY.jpeg', 'Silene Fajas.png', 'Super giros.png', 'Trade Business.jpeg', 'logo PSD negro completo 2r.png', 'logo-Learn-color.png', 'logo-TDM.png', 'logo1.png', 'logo_figdesis.jpg']
LOGO_ALT = ['AA SAS', 'Continental de Ingredientes', 'ED', 'Lockton Sekuritas', 'Droguería San Jorge', 'Eniwork', 'Ensalud', 'Los Olivos', 'Procaps', 'Rutina', 'Sushi Break', 'Manufacturas Económicas', 'QI Energy', 'Silene Fajas', 'Super Giros', 'Trade Business', 'PSD', 'Learn', 'TDM', 'Cliente', 'Figdesis']

def logos_block(title='Empresas que han confiado en este trabajo'):
    one = ''.join(f'<img src="{{R}}img/clientes/{slug(f)}.webp" alt="{esc(a)}" />' for f, a in zip(LOGOS, LOGO_ALT))
    two = ''.join(f'<img src="{{R}}img/clientes/{slug(f)}.webp" alt="" aria-hidden="true" />' for f in LOGOS)
    return f'''<section class="section tight bg-white">
  <div class="wrap center"><p class="eyebrow">{title}</p></div>
  <div class="logos" style="margin-top:18px"><div class="logos-track">{one}{two}</div></div>
</section>'''

QUOTES = [
 ('Las herramientas que nos ha brindado Marcela son un gran tesoro. Los resultados son a otro nivel.', 'Carmen Julia Cadena', 'Gerente General — Cheviotto Textil SAS', 'empresa'),
 ('Hoy trabajamos con un tractor, antes con un azadón. Marcela nos transformó como equipo y como empresa.', 'Javier Alberto Correa S.', 'Cheviotto Textil SAS', 'empresa'),
 ('Llegué con miedos que me paralizaban. Hoy tomo decisiones con claridad y estoy a días de cumplir un sueño que había postergado por años.', 'Alan Hernández Lagunas', 'Empresario — Estado de Guerrero, México', 'persona'),
 ('El seminario de Marcela me enseñó que si trabajamos nuestros pensamientos, los resultados cambian. Hoy manejo mejor mis emociones.', 'José Alexander Suárez', 'Empresario — Cali, Colombia', 'empresa'),
 ('Marcela me devolvió la fe en mí misma cuando más lo necesitaba. Doy gracias a Dios por ponerla en mi camino.', 'Sofía López', 'Febrero 2020', 'persona'),
 ('Gracias por enseñarme que la base de todo es vivir desde la gratitud. Invertir en mí a tu lado fue una de las mejores decisiones de mi vida.', 'Diana', 'Programa de Transformación Personal', 'persona'),
 ('Marcela me ayudó a entender que mis acciones venían del ego. Cambiar mis pensamientos cambió mi vida por completo.', 'Daniel Cárdenas', 'MBA — Nashville, USA', 'persona'),
]

def quotes_html(items):
    return '<div class="quotes">' + ''.join(f'<figure class="quote reveal"><p>{esc(q)}</p><cite><strong>{esc(n)}</strong>{esc(c)}</cite></figure>' for q, n, c, _ in items) + '</div>'

def testimonials_block(kind=None, title='Lo que dicen quienes ya dieron el paso'):
    items = [q for q in QUOTES if kind is None or q[3] == kind][:3]
    return f'''<section class="section bg-lav">
  <div class="wrap">
    {section_head('Testimonios', title, center=True)}
    {quotes_html(items)}
  </div>
</section>'''

# ================================================================= PÁGINAS
R = '{R}'

# ---------------- INICIO
home = hero(
  'Psicóloga · Mentora · Consultora',
  'Transforma tu manera de pensar, sentir y actuar. <em>Crea resultados extraordinarios.</em>',
  'Acompaño a personas, líderes y organizaciones en procesos de transformación personal y organizacional para convertir cambios internos en acciones y resultados sostenibles.',
  [('Quiero transformar mis resultados', R + 'coaching-personal/', 'btn-primary'), ('Soy empresa', '#empresas', 'btn-ghost')],
  'marcela-verde.webp', 'Marcela Córdoba, psicóloga y mentora en transformación personal y organizacional',
  badge='<strong>Modelo IDREA®</strong>Metodología propia de transformación', page_hero=False,
  proof=[('+15', 'años de experiencia'), ('+2.500', 'personas entrenadas'), ('+10', 'países')])
home += f'''
<section class="section bg-paper">
  <div class="wrap">
    <div class="callout reveal">
      <p class="eyebrow">¿Te reconoces?</p>
      <h2 class="h2">¿Sientes que puedes lograr más, pero <em>algo te está frenando?</em></h2>
      <p>Tal vez estás atravesando un cambio, repitiendo patrones, buscando mayor claridad, enfrentando nuevos retos de liderazgo o necesitas desarrollar el potencial de tu equipo.</p>
      <p class="punch">No necesitas más información. Necesitas identificar qué está bloqueando tus resultados y convertir esa conciencia en acciones poderosas.</p>
    </div>
  </div>
</section>

<section class="section bg-plum">
  <div class="wrap center reveal">
    <p class="eyebrow">La propuesta de valor</p>
    <p class="lead" style="font-size:1.2rem">No trabajo únicamente sobre el síntoma. Trabajo sobre la persona, sus relaciones y sus acciones para impactar los resultados.</p>
    <div class="formula" aria-label="Ser más relaciones más resultados"><span>SER</span><i>+</i><span>RELACIONES</span><i>+</i><span>RESULTADOS</span></div>
    <p class="lead" style="font-family:var(--font-display);font-style:italic;font-size:1.3rem;color:var(--lavender)">Porque los resultados extraordinarios comienzan con las personas que los crean.</p>
  </div>
</section>

<section class="section bg-paper" id="empresas">
  <div class="wrap">
    {section_head('Dos caminos', 'Encuentra el proceso <em>para ti</em>', center=True)}
    <div class="paths">
      <article class="path path-person reveal">
        <span class="path-num" aria-hidden="true">01</span>
        <p class="path-tag">Si eres persona</p>
        <h3 class="h3">Coaching personal</h3>
        <p>Un proceso para recuperar claridad, transformar patrones y crear resultados extraordinarios.</p>
        <div class="path-links"><a href="{R}coaching-personal/">Conocer el coaching personal</a></div>
      </article>
      <article class="path path-company reveal">
        <span class="path-num" aria-hidden="true">02</span>
        <p class="path-tag">Si representas una empresa</p>
        <h3 class="h3">Liderazgo • Formación • Selección</h3>
        <p>Soluciones para desarrollar personas, fortalecer equipos y atraer el talento adecuado.</p>
        <div class="path-links">
          <a href="{R}coaching-lideres/">Coaching para líderes</a>
          <a href="{R}formacion-desarrollo-talento/">Talleres y programas de formación</a>
          <a href="{R}seleccion-talento/">Atracción y selección de talento</a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section bg-white">
  <div class="wrap authority">
    <div class="reveal">
      <p class="eyebrow">Autoridad</p>
      <h2 class="h2">¿Por qué <em>Marcela</em>?</h2>
      <ul class="cred-list">
        <li><strong>Psicóloga</strong></li>
        <li><strong>Coach certificada</strong> internacionalmente</li>
        <li><strong>Mentora y consultora</strong> en transformación personal y organizacional</li>
        <li><strong>Creadora</strong> del Modelo IDREA®</li>
        <li><strong>Autora</strong> de RESULTADOS EXTRAORDINARIOS</li>
        <li><strong>Conferencista</strong> internacional</li>
      </ul>
    </div>
    <div class="reveal">
      <div class="stats-band">
        <div><strong>+15</strong><span>años de experiencia</span></div>
        <div><strong>+2.500</strong><span>personas entrenadas</span></div>
        <div><strong>+10</strong><span>países con empresas y equipos</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section bg-plum">
  <div class="wrap">
    {section_head('Metodología propia', 'Modelo <em>IDREA®</em>', 'Una metodología propia para pasar de la conciencia a la transformación y de la transformación a la acción.', center=True)}
    <div class="idrea-row">
      <div class="idrea-item reveal"><div class="idrea-letter">I</div><h3>Identificación</h3><p>Dónde estás hoy y qué bloquea tus resultados.</p></div>
      <div class="idrea-item reveal"><div class="idrea-letter">D</div><h3>Despertar consciente</h3><p>Tu historia, patrones y decisiones.</p></div>
      <div class="idrea-item reveal"><div class="idrea-letter">R</div><h3>Reprogramación</h3><p>Nuevas creencias, nuevas posibilidades.</p></div>
      <div class="idrea-item reveal"><div class="idrea-letter">E</div><h3>Emociones</h3><p>Reconocer y gestionar con conciencia.</p></div>
      <div class="idrea-item reveal"><div class="idrea-letter">A</div><h3>Acciones poderosas</h3><p>Transformación que se vuelve resultado.</p></div>
    </div>
    <div class="btn-row" style="justify-content:center"><a class="btn btn-light" href="{R}modelo-idrea/">Conoce el modelo IDREA®</a></div>
  </div>
</section>
{testimonials_block()}
{logos_block()}
<section class="section bg-paper"><div class="wrap"><div class="cta-band reveal">
  <h2 class="h2">La transformación comienza con <em>una decisión.</em></h2>
  <p>La pregunta no es solamente qué quieres cambiar. Es quién necesitas convertirte para crear los resultados que quieres.</p>
  <div class="btn-row"><a class="btn btn-light" href="{R}contacto/">Quiero dar el primer paso</a></div>
</div></div></section>'''

PERSON_LD = {
  '@context': 'https://schema.org',
  '@graph': [
    {'@type': 'Person', '@id': SITE + '/#marcela', 'name': 'Marcela Córdoba', 'jobTitle': 'Psicóloga, mentora y consultora en transformación personal y organizacional',
     'url': SITE + '/', 'image': SITE + '/img/marcela-verde.webp', 'alumniOf': 'Pontificia Universidad Javeriana',
     'sameAs': [u for _, _, u in SOCIAL]},
    {'@type': 'ProfessionalService', 'name': 'Marcela Córdoba', 'url': SITE + '/', 'founder': {'@id': SITE + '/#marcela'},
     'areaServed': 'Latinoamérica', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Cali', 'addressCountry': 'CO'},
     'description': 'Coaching personal, coaching para líderes, formación y desarrollo de talento, y atracción y selección de talento. Modelo IDREA®.'}
  ]}

page('', 'Marcela Córdoba | Transformación Personal y Organizacional en LATAM',
     'Psicóloga, mentora y consultora experta en transformación personal y organizacional. Coaching, liderazgo, desarrollo de talento y selección. Conoce el Modelo IDREA®.',
     'inicio', home, mobile_cta=('Quiero dar el primer paso', 'contacto/'), jsonld=PERSON_LD)

# ---------------- SOBRE MARCELA
sobre = hero('Sobre Marcela', 'Transformar personas para <em>transformar resultados.</em>',
  'Soy Marcela Córdoba, psicóloga, mentora y consultora experta en transformación personal y organizacional. Mi propósito es acompañar a personas, líderes y organizaciones a desarrollar su potencial y crear resultados extraordinarios.',
  [('Quiero hablar con Marcela', R + 'contacto/', 'btn-primary')], 'marcela-blazer.webp', 'Marcela Córdoba',
  badge='<strong>+15 años</strong>acompañando procesos de desarrollo humano y organizacional')
sobre += f'''
<section class="section bg-paper">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Mi enfoque</p>
      <h2 class="h2">Ser + relaciones + <em>resultados</em></h2>
    </div>
    <div class="prose reveal">
      <p class="lead">Mi fórmula de trabajo integra el SER + las relaciones + los resultados.</p>
      <p>Creo que una transformación sostenible comienza cuando la persona toma conciencia de su realidad, identifica lo que necesita cambiar y convierte esa conciencia en nuevas acciones.</p>
    </div>
  </div>
</section>

<section class="section bg-white">
  <div class="wrap split wide-left">
    <div class="reveal">
      <p class="eyebrow">Trayectoria y autoridad</p>
      <h2 class="h2" style="margin-bottom:28px">Una vida dedicada a la <em>transformación</em></h2>
      <ul class="arrow-list">
        <li>Más de 15 años de experiencia acompañando procesos de desarrollo humano y organizacional.</li>
        <li>Más de 2.500 personas entrenadas.</li>
        <li>Experiencia acompañando empresas, empresarios, líderes y equipos en más de 10 países.</li>
        <li>Creadora del Modelo de Transformación IDREA®.</li>
        <li>Autora del libro RESULTADOS EXTRAORDINARIOS.</li>
        <li>Psicóloga — Pontificia Universidad Javeriana.</li>
        <li>Formación avanzada en Recursos Humanos, coaching transformacional y PNL.</li>
      </ul>
    </div>
    <div class="reveal"><img src="{R}img/marcela-libro-jardin.webp" alt="Marcela Córdoba con su libro Resultados Extraordinarios" loading="lazy" style="margin:0 auto;max-height:560px;width:auto;border-radius:200px 200px 24px 24px;box-shadow:var(--shadow)" /></div>
  </div>
</section>

<section class="section bg-cream">
  <div class="wrap">
    {section_head('Formación', 'Formación académica y <em>complementaria</em>', center=True)}
    <div class="split" style="align-items:start;gap:24px">
      <div class="fact reveal"><p class="k">Académica</p>
        <ul class="arrow-list" style="margin-top:8px">
          <li>Psicóloga — Pontificia Universidad Javeriana</li>
          <li>Dirección de Recursos Humanos, Master Executive — Escuela Europea de Negocios</li>
          <li>Especialización en Administración de Empresas — Universidad del Rosario</li>
        </ul></div>
      <div class="fact reveal"><p class="k">Complementaria</p>
        <ul class="arrow-list" style="margin-top:8px">
          <li>UPW, Unleash the Power Within — Anthony Robbins, USA 2024</li>
          <li>Certificación Joe Dispenza 2022–2023</li>
          <li>Maestría de Coaching Transformacional Avanzado — KHI 2016</li>
          <li>Licensed NLP Coach — The Society of Neuro-Linguistic Programming, USA 2009</li>
        </ul></div>
    </div>
  </div>
</section>

<section class="section bg-plum">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Qué me diferencia</p>
      <h2 class="h2">No es solo motivación. <em>Es transformación.</em></h2>
    </div>
    <div class="reveal">
      <p class="lead">Integro psicología, coaching, desarrollo de talento, liderazgo y experiencia organizacional para acompañar cambios que puedan llevarse a la vida y al trabajo.</p>
    </div>
  </div>
</section>
{logos_block()}
{cta_band('¿Hablamos de lo que <em>quieres transformar</em>?', 'Cuéntame qué quieres transformar y encontremos el proceso adecuado para ti.', 'Quiero hablar con Marcela', R + 'contacto/')}'''
page('sobre-marcela/', 'Sobre Marcela Córdoba | Psicóloga, mentora y consultora',
     'Psicóloga de la Javeriana, coach certificada y creadora del Modelo IDREA®. Más de 15 años y más de 2.500 personas entrenadas en más de 10 países.',
     'sobre', sobre, mobile_cta=('Quiero hablar con Marcela', '../contacto/'))

# ---------------- MODELO IDREA
IDREA = [
 ('I', 'Identificación', 'Reconocemos dónde estás hoy, hacia dónde quieres ir y qué puede estar bloqueando tus resultados.'),
 ('D', 'Despertar consciente', 'Tomas conciencia de tu historia, patrones, decisiones y del impacto que tienes sobre tus resultados.'),
 ('R', 'Reprogramación', 'Trabajamos pensamientos y creencias limitantes para construir nuevas posibilidades de acción.'),
 ('E', 'Emociones', 'Aprendes a reconocer y gestionar tus emociones con mayor conciencia.'),
 ('A', 'Acciones poderosas', 'Convertimos la transformación en acciones concretas que generan resultados.'),
]
steps_html = ''.join(f'<div class="idrea-step reveal"><span class="big" aria-hidden="true">{l}</span><div><h2>{l} — {t}</h2><p>{d}</p></div></div>' for l, t, d in IDREA)
idrea = hero('Metodología propia', 'Modelo <em>IDREA®</em>', 'Una metodología de transformación para crear resultados extraordinarios.',
  [('Quiero conocer qué proceso es para mí', R + 'contacto/', 'btn-primary')], 'marcela-presenta.webp', 'Marcela Córdoba presentando el Modelo IDREA', flip=True,
  badge='<strong>5 movimientos</strong>de la conciencia a la acción')
idrea += f'''
<section class="section bg-paper">
  <div class="wrap">
    {section_head('Cinco movimientos', 'IDREA® integra cinco movimientos de <em>transformación</em>')}
    <div class="idrea-steps">{steps_html}</div>
  </div>
</section>
{statement('Resultado', 'Pasar de saber que necesitas cambiar a <em>comenzar a vivir, liderar y actuar</em> de una manera diferente.')}
<section class="section bg-cream">
  <div class="wrap">
    {section_head('Dónde se aplica', 'IDREA® en cada <em>proceso</em>', 'El modelo es el marco de trabajo del coaching personal, el coaching para líderes y los programas de formación para empresas.', center=True)}
    <div class="paths">
      <article class="path path-person reveal"><p class="path-tag">Personas</p><h3 class="h3">Coaching personal</h3><p>Programas de 3, 5, 8 o 12 sesiones.</p><div class="path-links"><a href="{R}coaching-personal/">Ver coaching personal</a></div></article>
      <article class="path path-company reveal"><p class="path-tag">Empresas</p><h3 class="h3">Líderes y equipos</h3><p>Coaching individual para líderes y programas de formación a la medida.</p><div class="path-links"><a href="{R}coaching-lideres/">Coaching para líderes</a><a href="{R}formacion-desarrollo-talento/">Formación y desarrollo</a></div></article>
    </div>
  </div>
</section>
{cta_band('¿Qué proceso es <em>para ti</em>?', 'Cuéntame qué quieres transformar y encontremos el proceso adecuado para ti.', 'Quiero conocer qué proceso es para mí', R + 'contacto/')}'''
page('modelo-idrea/', 'Modelo IDREA® | Metodología de transformación de Marcela Córdoba',
     'IDREA®: Identificación, Despertar consciente, Reprogramación, Emociones y Acciones poderosas. La metodología de Marcela Córdoba para crear resultados extraordinarios.',
     'idrea', idrea, mobile_cta=('Quiero conocer qué proceso es para mí', '../contacto/'))

# ---------------- COACHING PERSONAL
f_personal = form_block('personal', 'Coaching personal', 'Cuéntame qué quieres <em>transformar</em>',
  'Con esta información podré entender tu situación y orientarte hacia el programa adecuado.',
  [
    {'name': 'nombre', 'label': 'Nombre completo', 'req': True, 'ac': 'name'},
    {'name': 'correo', 'label': 'Correo electrónico', 'type': 'email', 'req': True, 'ac': 'email'},
    {'name': 'whatsapp', 'label': 'WhatsApp / teléfono', 'type': 'tel', 'req': True, 'ac': 'tel'},
    {'name': 'pais_ciudad', 'label': 'País y ciudad', 'req': True, 'ph': 'Ej.: Colombia, Cali'},
    {'name': 'situacion', 'label': '¿Qué situación quieres transformar?', 'type': 'textarea', 'req': True, 'full': True},
    {'name': 'resultado_esperado', 'label': '¿Qué resultado quieres lograr?', 'type': 'textarea', 'req': True, 'full': True},
    {'name': 'nivel_acompanamiento', 'label': '¿Qué nivel de acompañamiento estás buscando?', 'type': 'chips', 'opts': ['3 sesiones', '5 sesiones', '8 sesiones', '12 sesiones', 'No lo sé'], 'full': True},
  ],
  [
    {'name': 'que_ha_intentado', 'label': '¿Qué has intentado hasta ahora?', 'type': 'textarea', 'full': True},
    dict(ORIGEN, full=True),
  ], 'Quiero dar el primer paso')

personal = hero('Coaching personal', 'Resultados extraordinarios <em>comienzan en ti.</em>',
  'Un proceso de coaching transformacional para personas que quieren dejar de repetir patrones, recuperar claridad y crear una vida con mayor propósito y resultados.',
  [('Quiero dar el primer paso', '#formulario', 'btn-primary')], 'marcela-corazon.webp', 'Marcela Córdoba',
  badge='<strong>Virtual o presencial</strong>Programas de 3 a 12 sesiones')
personal += f'''
<section class="section bg-paper">
  <div class="wrap">
    {section_head('Identificación', '¿Esto te está <em>pasando</em>?')}
    {checks(['Te sientes estancado/a.', 'Sabes que puedes dar mucho más.', 'Repites patrones que ya no quieres seguir viviendo.', 'Quieres mejorar tus relaciones.', 'Quieres aumentar tus ingresos o abrir nuevas posibilidades.', 'Quieres volver a creer en ti.', 'Estás atravesando una reestructuración laboral o un cambio importante.'], 'two mirror')}
  </div>
</section>

<section class="section bg-white">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Qué es y para quién</p>
      <h2 class="h2">Un proceso para <em>ti</em>, no una charla motivacional</h2>
      <p class="lead" style="margin-top:18px">Es un acompañamiento individual de coaching transformacional, basado en el Modelo IDREA®, para personas que quieren pasar de saber que necesitan cambiar a actuar de una manera diferente.</p>
    </div>
    <div class="reveal">
      <p class="eyebrow">¿Qué puedes lograr?</p>
      <ul class="arrow-list">
        <li>Tomar decisiones con mayor seguridad.</li>
        <li>Dejar de autosabotearte.</li>
        <li>Gestionar tus emociones con mayor conciencia.</li>
        <li>Recuperar claridad y confianza.</li>
        <li>Actuar con intención.</li>
        <li>Construir resultados más sostenibles.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section bg-cream">
  <div class="wrap">
    {section_head('¿Cómo funciona?', 'Programas de <em>transformación</em>', 'Programas de 3, 5, 8 o 12 sesiones, definidos según el nivel de acompañamiento que necesites.')}
    <div class="programs">
      <article class="program reveal"><div class="program-n">3<small>sesiones</small></div><h3>Impulso Extraordinario</h3><p>Claridad y desbloqueo de un tema específico.</p></article>
      <article class="program reveal"><div class="program-n">5<small>sesiones</small></div><h3>Resultados en Acción</h3><p>Transformación de hábitos y comienzo de un cambio profundo.</p></article>
      <article class="program reveal"><div class="program-n">8<small>sesiones</small></div><h3>Expansión Extraordinaria</h3><p>Romper patrones y acelerar resultados.</p></article>
      <article class="program reveal"><div class="program-n">12<small>sesiones</small></div><h3>Resultados Extraordinarios</h3><p>Proceso de transformación integral.</p></article>
    </div>
    <p class="note reveal"><strong>Qué incluye:</strong> los programas incluyen diferentes niveles de acompañamiento, herramientas de entrenamiento y, según el programa, diagnóstico, formatos de registro, ejercicios de liberación y trabajo de raíces emocionales.</p>
    <div class="btn-row reveal"><a class="btn btn-primary" href="#formulario">Quiero saber qué programa es para mí</a></div>
  </div>
</section>

<section class="section bg-plum">
  <div class="wrap">
    {section_head('Metodología', 'El camino <em>IDREA®</em>', center=True)}
    <div class="idrea-row">
      {''.join(f'<div class="idrea-item reveal"><div class="idrea-letter">{l}</div><h3>{t}</h3><p>{d}</p></div>' for l, t, d in IDREA)}
    </div>
  </div>
</section>
{authority_block()}
{testimonials_block('persona')}
{how_to_hire('persona')}
{f_personal}'''
page('coaching-personal/', 'Coaching personal | Marcela Córdoba',
     'Coaching transformacional para dejar de repetir patrones, recuperar claridad y crear resultados extraordinarios. Programas de 3, 5, 8 o 12 sesiones. Virtual o presencial.',
     'personal', personal, mobile_cta=('Quiero dar el primer paso', '#formulario'),
     jsonld={'@context': 'https://schema.org', '@type': 'Service', 'name': 'Coaching personal', 'provider': {'@type': 'Person', 'name': 'Marcela Córdoba'}, 'areaServed': 'Latinoamérica', 'url': SITE + '/coaching-personal/'})

# ---------------- COACHING PARA LÍDERES
f_lideres = form_block('lideres', 'Coaching para líderes', 'Hablemos sobre un <em>líder</em> de tu empresa',
  'Cuéntanos el reto de liderazgo y el resultado que esperan. Con esto preparamos una conversación útil desde el primer contacto.',
  company_base() + [
    {'name': 'reto_liderazgo', 'label': '¿Cuál es el principal reto de liderazgo?', 'type': 'textarea', 'req': True, 'full': True},
    {'name': 'comportamientos_a_transformar', 'label': '¿Qué comportamientos o resultados quieren transformar?', 'type': 'textarea', 'req': True, 'full': True},
    {'name': 'resultado_esperado', 'label': '¿Qué resultado esperan del proceso?', 'type': 'textarea', 'req': True, 'full': True},
  ],
  [
    {'name': 'lider_a_acompanar', 'label': 'Nombre y cargo del líder a acompañar'},
    {'name': 'numero_de_lideres', 'label': 'Número de líderes a acompañar', 'type': 'number'},
    MODALIDAD,
    dict(ORIGEN_E, full=True),
  ], 'Quiero una propuesta',
  reassure=['Respuesta con una propuesta según el reto de su líder.', 'Modalidad virtual o presencial.', 'Sus datos se usan solo para responder la solicitud.'])

lideres = hero('Coaching para líderes en empresas', 'Liderazgo consciente: <em>transforma la manera en que lideras.</em>',
  'Acompañamiento individual para líderes que quieren fortalecer su comunicación, gestionar mejor sus emociones, conectar con su equipo y generar resultados diferentes.',
  [('Quiero fortalecer mi liderazgo', '#formulario', 'btn-primary')], 'marcela-senala.webp', 'Marcela Córdoba', flip=False,
  badge='<strong>5 sesiones</strong>Programa individual para líderes')
lideres += f'''
<section class="section bg-paper">
  <div class="wrap">
    {section_head('Identificación', '¿Tu reto como líder <em>es…</em>?')}
    {checks(['Lograr mayor compromiso de tu equipo.', 'Comunicarte de manera más efectiva.', 'Tener conversaciones difíciles.', 'Delegar y poner límites.', 'Gestionar conflictos y tensiones.', 'Fortalecer tu influencia.', 'Mejorar las relaciones y el clima del equipo.', 'Convertirte en un líder más consciente y efectivo.'], 'two mirror')}
  </div>
</section>

<section class="section bg-white">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Qué es y para quién</p>
      <h2 class="h2">Un proceso individual para <em>líderes</em> que quieren resultados diferentes</h2>
      <p class="lead" style="margin-top:18px">Para gerentes, directores y líderes de equipo que la empresa quiere fortalecer. El proceso trabaja sobre la persona, sus relaciones y sus acciones con el Modelo IDREA® como marco.</p>
    </div>
    <div class="reveal">
      <p class="eyebrow">¿Qué trabajamos?</p>
      <ul class="arrow-list">
        <li>Transformación mental y emocional.</li>
        <li>Comunicación y conexión con el equipo.</li>
        <li>Competencias de liderazgo.</li>
        <li>Creencias y patrones que pueden limitar el desempeño.</li>
        <li>Gestión emocional.</li>
        <li>Plan de acción orientado a resultados.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section bg-cream">
  <div class="wrap">
    {section_head('Formato', 'Cómo funciona y <em>qué incluye</em>')}
    <div class="facts">
      <div class="fact reveal"><p class="k">Programa</p><p class="v">Individual de 5 sesiones</p></div>
      <div class="fact reveal"><p class="k">Duración</p><p class="v">Sesiones de aprox. 1 h 15 min, o más cuando la situación lo requiera</p></div>
      <div class="fact reveal"><p class="k">Modalidad</p><p class="v">Virtual o presencial, con acompañamiento puntual vía WhatsApp o teléfono</p></div>
    </div>
  </div>
</section>
{statement('Resultado buscado', 'Un líder que se siente <em>protagonista de sus resultados</em>, conecta con su equipo y cuenta con herramientas para liderar de manera más consciente.')}
{authority_block()}
{logos_block()}
{how_to_hire('empresa')}
<section class="section tight bg-cream" style="padding-top:0"><div class="wrap center"><a class="btn btn-primary" href="#formulario">Quiero hablar sobre un líder de mi empresa</a></div></section>
{f_lideres}'''
page('coaching-lideres/', 'Coaching para líderes | Liderazgo consciente — Marcela Córdoba',
     'Coaching ejecutivo individual para líderes: comunicación, gestión emocional, conversaciones difíciles y resultados. Programa de 5 sesiones, virtual o presencial.',
     'lideres', lideres, mobile_cta=('Quiero fortalecer mi liderazgo', '#formulario'),
     jsonld={'@context': 'https://schema.org', '@type': 'Service', 'name': 'Coaching para líderes', 'provider': {'@type': 'Person', 'name': 'Marcela Córdoba'}, 'areaServed': 'Latinoamérica', 'url': SITE + '/coaching-lideres/'})

# ---------------- FORMACIÓN Y DESARROLLO
f_form = form_block('formacion', 'Formación y desarrollo de talento', 'Diseñemos un programa para <em>tu empresa</em>',
  'Cuéntanos qué está pasando en tu equipo y qué resultado quieren lograr. Diseñamos la experiencia a partir de su contexto real.',
  company_base() + [
    {'name': 'participantes', 'label': 'Número aproximado de participantes', 'type': 'number', 'req': True},
    {'name': 'tema', 'label': 'Tema o competencia que desean desarrollar', 'req': True, 'ph': 'Ej.: liderazgo, comunicación…'},
    {'name': 'situacion_actual', 'label': '¿Qué está pasando actualmente?', 'type': 'textarea', 'req': True, 'full': True},
    {'name': 'resultado_esperado', 'label': '¿Qué resultado quieren lograr?', 'type': 'textarea', 'req': True, 'full': True},
  ],
  [
    {'name': 'duracion', 'label': 'Duración aproximada', 'type': 'chips', 'opts': ['2 horas', '4 horas', 'Varias sesiones', 'Por definir'], 'full': True},
    dict(MODALIDAD, label='Modalidad'),
    {'name': 'fecha_aproximada', 'label': 'Fecha aproximada del proceso', 'ph': 'Ej.: febrero 2027'},
    {'name': 'ciudad_pais', 'label': 'Ciudad / país'},
    dict(ORIGEN_E, full=True),
  ], 'Quiero una propuesta',
  reassure=['Experiencias diseñadas a la medida de la organización.', 'Virtual o presencial, en Colombia y LATAM.', 'Sus datos se usan solo para responder la solicitud.'])

formacion = hero('Talleres y programas de formación', 'Desarrolla el potencial de tu equipo. <em>Transforma sus resultados.</em>',
  'Diseñamos talleres y programas de formación prácticos y experienciales para fortalecer personas, líderes y equipos según los desafíos reales de cada organización.',
  [('Quiero desarrollar mi equipo', '#formulario', 'btn-primary')], 'marcela-presenta.webp', 'Marcela Córdoba', flip=True,
  badge='<strong>A la medida</strong>Talleres, jornadas y programas')
formacion += f'''
<section class="section bg-paper">
  <div class="wrap">
    {section_head('Identificación', '¿Qué quieres transformar <em>en tu equipo</em>?')}
    {checks(['Liderazgo.', 'Comunicación.', 'Trabajo en equipo.', 'Inteligencia emocional.', 'Gestión de conflictos.', 'Colaboración y compromiso.', 'Equipos de alto desempeño.', 'Servicio y excelencia.', 'Cultura de responsabilidad y resultados.'], 'three')}
  </div>
</section>

<section class="section bg-white">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Nuestra metodología</p>
      <h2 class="h2">Cada experiencia se diseña a partir de <em>su contexto</em></h2>
      <p class="lead" style="margin-top:18px">Partimos del contexto, objetivo y necesidad de la organización, utilizando el Modelo IDREA® como marco de transformación.</p>
    </div>
    <div class="reveal">
      <ul class="arrow-list">
        <li>Identificación de realidad, bloqueos y oportunidades.</li>
        <li>Despertar consciente sobre el impacto personal y colectivo.</li>
        <li>Reprogramación de pensamientos y creencias limitantes.</li>
        <li>Gestión emocional para fortalecer relaciones y liderazgo.</li>
        <li>Acciones poderosas y compromisos concretos.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section bg-cream">
  <div class="wrap">
    {section_head('Formatos', 'Qué <em>incluye</em>')}
    {checks(['Talleres de alto impacto para necesidades puntuales.', 'Jornadas de formación.', 'Programas de varias sesiones.', 'Programas para líderes.', 'Procesos de desarrollo de equipos de alto desempeño.', 'Experiencias diseñadas a la medida.'], 'three')}
  </div>
</section>
{statement('Principio', 'La formación no debe quedarse en el salón. Debe convertirse en <em>nuevas maneras de pensar, relacionarse y actuar.</em>')}
{authority_block()}
{logos_block()}
{testimonials_block('empresa', 'Equipos y empresas que ya lo vivieron')}
{how_to_hire('empresa')}
<section class="section tight bg-cream" style="padding-top:0"><div class="wrap center"><a class="btn btn-primary" href="#formulario">Quiero diseñar un programa para mi empresa</a></div></section>
{f_form}'''
page('formacion-desarrollo-talento/', 'Talleres y formación empresarial | Desarrollo de talento — Marcela Córdoba',
     'Talleres y programas de formación a la medida: liderazgo, comunicación, inteligencia emocional y equipos de alto desempeño, con el Modelo IDREA®.',
     'formacion', formacion, mobile_cta=('Quiero desarrollar mi equipo', '#formulario'),
     jsonld={'@context': 'https://schema.org', '@type': 'Service', 'name': 'Talleres y programas de formación y desarrollo de talento', 'provider': {'@type': 'Person', 'name': 'Marcela Córdoba'}, 'areaServed': 'Latinoamérica', 'url': SITE + '/formacion-desarrollo-talento/'})

# ---------------- SELECCIÓN
f_sel = form_block('seleccion', 'Atracción y selección de talento', 'Iniciemos tu proceso de <em>selección</em>',
  'Con estos datos revisamos el cargo y te presentamos cómo sería la búsqueda.',
  company_base() + [
    {'name': 'cargo_a_seleccionar', 'label': 'Cargo a seleccionar', 'req': True},
    {'name': 'numero_de_vacantes', 'label': 'Número de vacantes', 'type': 'number', 'req': True},
    {'name': 'ciudad_pais', 'label': 'Ciudad / país', 'req': True},
    {'name': 'fecha_para_cubrir', 'label': 'Fecha estimada para cubrir la vacante', 'type': 'date', 'req': True},
    {'name': 'necesidad', 'label': 'Descripción breve de la necesidad', 'type': 'textarea', 'req': True, 'full': True},
  ],
  [
    {'name': 'existe_perfil', 'label': '¿Existe descripción y perfil del cargo?', 'type': 'chips', 'opts': ['Sí', 'No'], 'full': True},
    {'name': 'nivel_del_cargo', 'label': 'Tipo de cargo / nivel', 'type': 'select', 'opts': ['Operativo', 'Técnico / profesional', 'Coordinación / jefatura', 'Gerencial / directivo', 'Otro']},
    {'name': 'rango_salarial', 'label': 'Salario o rango salarial (opcional)'},
    dict(ORIGEN_E, full=True),
  ], 'Quiero iniciar un proceso de selección',
  reassure=['Duración estimada de 20 días según la búsqueda.', 'Terna final con informes por candidato.', 'Sus datos se usan solo para responder la solicitud.'])

phases = ''.join(f'<div class="phase reveal"><b>{i}</b><p>{t}</p></div>' for i, t in enumerate(['Revisión y análisis del cargo.', 'Localización de candidatos.', 'Preselección.', 'Entrevistas por competencias y pruebas psicotécnicas.', 'Informes finales y presentación de terna de candidatos.'], 1))
seleccion = hero('Atracción y selección de talento', 'Encuentra a la persona adecuada para el cargo <em>y para tu organización.</em>',
  'Un proceso integral de atracción y selección para identificar talento alineado con las necesidades del cargo y los objetivos de la organización.',
  [('Quiero iniciar un proceso de selección', '#formulario', 'btn-primary')], 'marcela-pensativa.webp', 'Marcela Córdoba',
  badge='<strong>20 días</strong>duración estimada de la búsqueda')
seleccion += f'''
<section class="section bg-paper">
  <div class="wrap">
    {section_head('Identificación', '¿Necesitas cubrir una vacante y quieres <em>tomar una buena decisión</em>?')}
    {checks(['Tienes una vacante y necesitas cubrirla con criterio.', 'Recibes hojas de vida pero no sabes cuáles realmente cumplen el perfil.', 'Necesitas definir claramente el perfil del cargo.', 'Quieres evaluar conocimientos, experiencia y competencias.', 'Quieres reducir el riesgo de una contratación inadecuada.'], 'two mirror')}
  </div>
</section>

<section class="section bg-plum">
  <div class="wrap">
    {section_head('Evaluamos tres dimensiones', 'Saber + Hacer + <em>Ser</em>', center=True)}
    <div class="dims">
      <div class="dim reveal"><strong>SABER</strong><span>Conocimientos y formación.</span></div>
      <div class="dim reveal"><strong>HACER</strong><span>Experiencia y capacidades para desempeñar el rol.</span></div>
      <div class="dim reveal"><strong>SER</strong><span>Competencias, comportamientos, motivaciones y características relevantes para el cargo.</span></div>
    </div>
  </div>
</section>

<section class="section bg-paper">
  <div class="wrap">
    {section_head('Cómo funciona', 'Nuestro proceso en <em>5 fases</em>', center=True)}
    <div class="phases">{phases}</div>
    <p class="duration reveal">Duración estimada: <strong>20 días</strong>, de acuerdo con las características de la búsqueda.</p>
  </div>
</section>

<section class="section bg-cream">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Valor agregado</p>
      <h2 class="h2">Acompañamiento <em>después</em> de la contratación</h2>
    </div>
    <div class="reveal">
      <p class="lead">Acompañamiento opcional mediante coaching de adaptación a la cultura y al cargo durante los primeros meses del candidato seleccionado.</p>
      <div class="btn-row"><a class="btn btn-primary" href="#formulario">Quiero iniciar un proceso de selección</a></div>
    </div>
  </div>
</section>
{authority_block(heading='¿Por qué <em>Marcela</em>?')}
{logos_block()}
{how_to_hire('empresa')}
{f_sel}'''
page('seleccion-talento/', 'Selección de personal | Atracción y selección de talento — Marcela Córdoba',
     'Proceso integral de selección de personal en 5 fases: análisis del cargo, búsqueda, preselección, entrevistas por competencias, pruebas y terna. Duración estimada de 20 días.',
     'seleccion', seleccion, mobile_cta=('Quiero iniciar un proceso de selección', '#formulario'),
     jsonld={'@context': 'https://schema.org', '@type': 'Service', 'name': 'Atracción y selección de talento', 'provider': {'@type': 'Person', 'name': 'Marcela Córdoba'}, 'areaServed': 'Latinoamérica', 'url': SITE + '/seleccion-talento/'})

# ---------------- CONTACTO
f_general = form_block('general', 'Contacto general', 'Cuéntanos qué <em>necesitas</em>',
  'Elige si eres persona o empresa y el servicio que te interesa. Te responderemos para definir el siguiente paso.',
  [
    {'name': 'nombre', 'label': 'Nombre completo', 'req': True, 'ac': 'name'},
    {'name': 'empresa', 'label': 'Empresa (si aplica)', 'ac': 'organization'},
    {'name': 'correo', 'label': 'Correo', 'type': 'email', 'req': True, 'ac': 'email'},
    {'name': 'whatsapp', 'label': 'WhatsApp / teléfono', 'type': 'tel', 'req': True, 'ac': 'tel'},
    {'name': 'soy', 'label': 'Soy', 'type': 'chips', 'opts': ['Persona', 'Empresa'], 'req': True, 'full': True},
    {'name': 'interes', 'label': 'Estoy interesado/a en', 'type': 'select', 'req': True, 'full': True, 'opts': ['Coaching personal', 'Coaching para líderes', 'Formación y desarrollo', 'Selección', 'Otro']},
    {'name': 'mensaje', 'label': 'Mensaje', 'type': 'textarea', 'req': True, 'full': True},
  ], [], 'Quiero hablar con Marcela')

contacto = hero('Contacto', 'Hablemos de lo que <em>quieres transformar.</em>',
  'Si estás buscando transformar algo en tu vida, fortalecer tu liderazgo, desarrollar tu equipo o encontrar el talento adecuado para tu organización, este puede ser el primer paso.',
  [('Quiero hablar con Marcela', '#formulario', 'btn-primary')], 'marcela-verde.webp', 'Marcela Córdoba',
  badge='<strong>Personas y empresas</strong>Atención virtual en LATAM y presencial en Colombia')
contacto += f'''
<section class="section tight bg-paper">
  <div class="wrap">
    {section_head('Opciones de contacto', 'Elige el canal <em>que prefieras</em>')}
    <div class="contact-options" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">
      <a href="#formulario" class="reveal">{ICONS['mail']}<div><small>Formulario</small><span>Escribir ahora</span></div></a>
      <a data-wa href="#" target="_blank" rel="noopener" class="reveal" data-wa-wrap>{ICONS['wa']}<div><small>WhatsApp</small><span data-phone></span></div></a>
      <a data-email-wrap class="reveal" href="#" data-email-link>{ICONS['mail']}<div><small>Correo electrónico</small><span data-email></span></div></a>
      <div class="reveal">{ICONS['pin']}<div><small>Ubicación / modalidad</small><span>Cali, Colombia · Virtual en LATAM</span></div></div>
    </div>
    <div class="socials" style="margin-top:28px;color:var(--purple)">{socials_html().replace('<a ', '<a style="border-color:var(--line)" ')}</div>
  </div>
</section>
{f_general}'''
page('contacto/', 'Contacto | Marcela Córdoba',
     'Hablemos de lo que quieres transformar: coaching personal, coaching para líderes, formación de equipos o selección de talento. Escríbenos o contáctanos por WhatsApp.',
     'contacto', contacto, mobile_cta=('Quiero hablar con Marcela', '#formulario'))

# ---------------- RECURSOS
mom = ''.join(f'<button type="button" aria-label="Ver foto {i} en grande"><img src="{R}img/momentos/momento-{i:02d}.webp" alt="Momento de transformación {i}" loading="lazy" /></button>' for i in range(1, 13))
recursos = hero('Recursos', 'Herramientas para seguir <em>transformando.</em>',
  'El libro RESULTADOS EXTRAORDINARIOS, testimonios de personas y empresas, y momentos de los procesos de transformación.',
  [('Conocer el libro', '#libro', 'btn-primary')], 'marcela-libro.webp', 'Marcela Córdoba con su libro Resultados Extraordinarios', flip=True,
  badge='<strong>Resultados Extraordinarios</strong>el libro de Marcela Córdoba')
recursos += f'''
<section class="section bg-paper" id="libro">
  <div class="wrap book">
    <div class="reveal"><img class="book-cover" src="{R}img/libro-portada.webp" alt="Portada del libro Resultados Extraordinarios de Marcela Córdoba" loading="lazy" /></div>
    <div class="reveal">
      <p class="eyebrow">El libro</p>
      <h2 class="h2">Resultados <em>Extraordinarios</em></h2>
      <p class="lead" style="margin:18px 0 26px">Un libro creado para inspirarte a transformar tu mentalidad, superar límites y diseñar una vida y un negocio con propósito y resultados extraordinarios.</p>
      <ul class="checks two"><li>Historias reales</li><li>Herramientas prácticas</li><li>Estrategias comprobadas</li><li>Transformación profunda</li></ul>
      <div class="btn-row"><a class="btn btn-primary" href="{R}contacto/">Quiero el libro</a></div>
    </div>
  </div>
</section>

<section class="section bg-lav">
  <div class="wrap">
    {section_head('Testimonios', 'Momentos de <em>transformación</em>', center=True)}
    <div class="videos">
      <video controls playsinline preload="none" poster="{R}poster/poster1.png"><source src="{R}testimonios/VideoTestimonio.mp4" type="video/mp4" /></video>
      <video controls playsinline preload="none" poster="{R}poster/poster2.png"><source src="{R}testimonios/VideoBuenoTestimonio2.mp4" type="video/mp4" /></video>
      <video controls playsinline preload="none" poster="{R}poster/poster3.png"><source src="{R}testimonios/VideoTestimonio3.mp4" type="video/mp4" /></video>
    </div>
    {quotes_html(QUOTES)}
  </div>
</section>

<section class="section bg-paper">
  <div class="wrap">
    {section_head('Galería', 'Galería de <em>momentos</em>', 'Instantes que capturan el camino hacia una vida más plena y auténtica.', center=True)}
    <div class="gallery">{mom}</div>
  </div>
</section>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Visor de fotos">
  <button class="lb-close" aria-label="Cerrar">✕</button><button class="lb-prev" aria-label="Anterior">‹</button>
  <img src="" alt="" /><button class="lb-next" aria-label="Siguiente">›</button>
</div>
{cta_band('La transformación comienza con <em>una decisión.</em>', 'Cuéntame qué quieres transformar y encontremos el proceso adecuado para ti.', 'Quiero dar el primer paso', R + 'contacto/')}'''
page('recursos/', 'Recursos | Libro Resultados Extraordinarios y testimonios — Marcela Córdoba',
     'El libro Resultados Extraordinarios de Marcela Córdoba, testimonios de personas y empresas, y galería de momentos de transformación.',
     'recursos', recursos, mobile_cta=('Quiero dar el primer paso', '../contacto/'))

# ---------------- POLÍTICA DE DATOS (plantilla — revisar con Marcela/abogado)
legal = '''<section class="section bg-paper"><div class="wrap legal">
<p class="eyebrow">Legal</p>
<h1 class="h2">Política de tratamiento de datos personales</h1>
<!-- PLANTILLA BASE (Ley 1581 de 2012 y Decreto 1377 de 2013). Debe ser revisada y completada por Marcela Córdoba antes de publicar. -->
<p>En cumplimiento de la Ley 1581 de 2012 y sus decretos reglamentarios, Marcela Córdoba informa la política aplicable al tratamiento de los datos personales que recibe a través de este sitio web y de sus canales de contacto.</p>
<h2>1. Responsable del tratamiento</h2>
<p>Marcela Córdoba, con domicilio en Cali, Colombia. Canales de contacto: los publicados en la página <a href="../contacto/">Contacto</a>.</p>
<h2>2. Datos que recolectamos</h2>
<p>Nombre, correo electrónico, teléfono o WhatsApp, país y ciudad, empresa y cargo (cuando aplica), y la información que la persona comparte voluntariamente en los formularios sobre su necesidad. También se registran la página de origen y la fuente de la visita.</p>
<h2>3. Finalidades</h2>
<ul>
<li>Responder solicitudes y contactar a la persona para entender su necesidad.</li>
<li>Presentar propuestas de servicios de coaching, formación, consultoría y selección.</li>
<li>Gestionar la relación comercial y el registro de contactos en sistemas de gestión de clientes (CRM).</li>
<li>Enviar información relacionada con los servicios, cuando la persona lo autorice.</li>
<li>Medir el funcionamiento del sitio web para mejorarlo.</li>
</ul>
<h2>4. Derechos del titular</h2>
<p>Como titular puedes conocer, actualizar, rectificar y solicitar la supresión de tus datos, revocar la autorización otorgada, solicitar prueba de la autorización, ser informado sobre el uso de tus datos y presentar quejas ante la Superintendencia de Industria y Comercio.</p>
<h2>5. Cómo ejercer tus derechos</h2>
<p>Puedes enviar tu consulta o reclamo a través de los canales publicados en la página de Contacto. Las consultas se atenderán en un máximo de diez (10) días hábiles y los reclamos en un máximo de quince (15) días hábiles, conforme a la ley.</p>
<h2>6. Seguridad y transferencia</h2>
<p>Los datos se almacenan con medidas razonables de seguridad y pueden ser procesados por proveedores tecnológicos (por ejemplo, servicios de formularios, correo o CRM) que actúan como encargados del tratamiento.</p>
<h2>7. Vigencia</h2>
<p>Esta política rige desde su publicación. Los datos se conservarán mientras sean necesarios para las finalidades descritas.</p>
</div></section>'''
page('politica-de-datos/', 'Política de tratamiento de datos | Marcela Córdoba',
     'Política de tratamiento de datos personales del sitio web de Marcela Córdoba, conforme a la Ley 1581 de 2012.',
     None, legal)

# ---------------- 404
nf = f'''<section class="section bg-paper" style="min-height:60vh;display:flex;align-items:center"><div class="wrap center">
<p class="eyebrow">Error 404</p><h1 class="h1">Esta página <em>no existe.</em></h1>
<p class="lead" style="margin-top:16px">Puede que el enlace haya cambiado. Te ayudamos a encontrar el camino.</p>
<div class="btn-row"><a class="btn btn-primary" href="/">Ir al inicio</a><a class="btn btn-ghost" href="/contacto/">Contacto</a></div>
</div></section>'''
# 404 usa rutas absolutas (GitHub Pages la sirve en cualquier URL)
with open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8') as f:
    pass
page('__404/', 'Página no encontrada | Marcela Córdoba', 'Página no encontrada.', None, nf, noindex=True)
src = open(os.path.join(OUT, '__404', 'index.html'), encoding='utf-8').read().replace('../', '/')
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(src)
import shutil; shutil.rmtree(os.path.join(OUT, '__404'))

# ---------------- sitemap / robots
urls = ['', 'sobre-marcela/', 'modelo-idrea/', 'coaching-personal/', 'coaching-lideres/', 'formacion-desarrollo-talento/', 'seleccion-talento/', 'recursos/', 'contacto/', 'politica-de-datos/']
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE}/{u}</loc><lastmod>2026-11-13</lastmod><priority>{"1.0" if u == "" else "0.8" if "politica" not in u else "0.2"}</priority></url>\n' for u in urls) + '</urlset>\n'
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print('ok')
