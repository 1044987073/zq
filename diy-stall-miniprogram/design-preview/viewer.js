(function () {
  const boards = window.DH_BOARDS || [];
  const tokens = window.DH_TOKENS || [];
  const boardsEl = document.getElementById('boards');
  const pageList = document.getElementById('pageList');
  const canvas = document.getElementById('canvas');
  const canvasWrap = document.getElementById('canvasWrap');
  const zoomLabel = document.getElementById('zoomLabel');
  const inspectName = document.getElementById('inspectName');
  const inspectDesc = document.getElementById('inspectDesc');
  const tokenEditors = document.getElementById('tokenEditors');

  let zoom = 0.55;
  let activeId = boards[0]?.id;

  function tabbarHtml(active) {
    const tabs = ['首页', '项目', '套餐', '关于'];
    const keys = ['home', 'catalog', 'bundles', 'about'];
    const idx = keys.indexOf(active);
    return `<div class="dh-tabbar">${tabs
      .map((t, i) => `<span class="${i === idx ? 'on' : ''}">${t}</span>`)
      .join('')}</div>`;
  }

  function renderBoards() {
    boardsEl.innerHTML = boards
      .map((b) => {
        const navTitle = b.name.split('·').pop().trim();
        const showTab = b.tab;
        return `
        <div class="dh-board" id="board-${b.id}" data-id="${b.id}">
          <div class="dh-board__label">${b.name}</div>
          <div class="dh-phone">
            <div class="dh-phone__status"></div>
            <div class="dh-phone__nav">${navTitle}</div>
            <div class="dh-phone__scroll">${b.html}</div>
            ${showTab ? tabbarHtml(b.id) : ''}
          </div>
        </div>`;
      })
      .join('');
  }

  function renderPageList() {
    pageList.innerHTML = boards
      .map(
        (b) => `
      <li class="dh-page-item ${b.id === activeId ? 'active' : ''}" data-id="${b.id}">
        <div class="dh-thumb"><div class="dh-thumb__bar"></div></div>
        <span>${b.name.replace('用户端 · ', '').replace('管理端 · ', '')}</span>
      </li>`
      )
      .join('');
    pageList.querySelectorAll('.dh-page-item').forEach((el) => {
      el.addEventListener('click', () => focusBoard(el.dataset.id));
    });
  }

  function renderTokens() {
    tokenEditors.innerHTML = tokens
      .map((t) => {
        const val = getComputedStyle(document.documentElement).getPropertyValue(t.var).trim() || '#000000';
        return `<div class="dh-token-row"><span>${t.label}</span><input type="color" data-var="${t.var}" value="${toHex(val)}" /></div>`;
      })
      .join('');
    tokenEditors.querySelectorAll('input').forEach((input) => {
      input.addEventListener('input', () => {
        document.documentElement.style.setProperty(input.dataset.var, input.value);
        syncPrimarySurfaces();
      });
    });
  }

  function toHex(css) {
    if (css.startsWith('#')) return css.length === 7 ? css : '#2d6a4f';
    return '#2d6a4f';
  }

  function syncPrimarySurfaces() {
    const primary = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim();
    document.querySelectorAll('.dh-phone__status, .dh-phone__nav, .dh-hero').forEach((el) => {
      el.style.background = primary;
    });
  }

  function applyZoom() {
    canvas.style.transform = `scale(${zoom})`;
    zoomLabel.textContent = `${Math.round(zoom * 100)}%`;
  }

  function focusBoard(id) {
    activeId = id;
    renderPageList();
    const b = boards.find((x) => x.id === id);
    if (b) {
      inspectName.textContent = b.name;
      inspectDesc.textContent = b.desc;
    }
    document.querySelectorAll('.dh-board').forEach((el) => {
      el.classList.toggle('focused', el.dataset.id === id);
    });
    const target = document.getElementById('board-' + id);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
    }
  }

  document.getElementById('zoomIn').addEventListener('click', () => {
    zoom = Math.min(1.2, zoom + 0.1);
    applyZoom();
  });
  document.getElementById('zoomOut').addEventListener('click', () => {
    zoom = Math.max(0.35, zoom - 0.1);
    applyZoom();
  });
  document.getElementById('zoomFit').addEventListener('click', () => {
    zoom = 0.55;
    applyZoom();
    if (activeId) focusBoard(activeId);
  });

  canvasWrap.addEventListener(
    'wheel',
    (e) => {
      if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        zoom += e.deltaY > 0 ? -0.05 : 0.05;
        zoom = Math.max(0.35, Math.min(1.2, zoom));
        applyZoom();
      }
    },
    { passive: false }
  );

  renderBoards();
  renderPageList();
  renderTokens();
  applyZoom();
  focusBoard(activeId);
})();
