# Generates share blocks (idempotent), feed.xml and llms.txt from the current site files.
import re, glob, html, json, os
from urllib.parse import quote
from email.utils import format_datetime
from datetime import datetime, timezone
root='/home/user/madry-portfel/'; BASE='https://bartuniadev.github.io/madry-portfel/'

def share_html(url, title):
    u=quote(url, safe=''); t=quote(title, safe='')
    return f'''  <div class="share" data-url="{url}" data-title="{html.escape(title)}">
    <p class="share-title">Przyda się komuś? Podeślij ten poradnik</p>
    <div class="share-links">
      <button type="button" data-share-native hidden>Udostępnij</button>
      <button type="button" data-share-copy>Kopiuj link</button>
      <a href="https://wa.me/?text={t}%20{u}" rel="noopener" target="_blank">WhatsApp</a>
      <a href="https://www.facebook.com/sharer/sharer.php?u={u}" rel="noopener" target="_blank">Facebook</a>
      <a href="https://www.linkedin.com/sharing/share-offsite/?url={u}" rel="noopener" target="_blank">LinkedIn</a>
      <a href="https://twitter.com/intent/tweet?url={u}&amp;text={t}" rel="noopener" target="_blank">X</a>
    </div>
    <p class="share-note" aria-live="polite"></p>
  </div>

'''

